"""
Author: Xinyi Yu, Yiqi Zhao
"""
import numpy as np
import math
from pyscipopt import Model
import json
from parameters import *

np.random.seed(12)

def generate_region_location():
    region_1 = [round(np.random.uniform(1.5, 2.5), 2), round(np.random.uniform(0.5, 1), 2)]
    region_2 = [round(np.random.uniform(2.5, 3.5), 2), round(np.random.uniform(4, 4.5), 2)]
    return [region_1, region_2]


def generate_sensor_ouput(location, sensor_noise):
    return [round(np.random.laplace(location[0], sensor_noise), 2), round(np.random.laplace(location[1], sensor_noise), 2)]

def is_successful_trajectory(trajectory_x, trajectory_y, region_location, num_region, region_distance):
    if max(math.sqrt((trajectory_x[time_point[n_o]] - region_location[n_o][0])**2 + (trajectory_y[time_point[n_o]] - region_location[n_o][1])**2) - region_distance for n_o in range(num_region)) > 0:
        # print("Oops! It did not arrive the required regions!")
        return False
    return True


def cp():
    """
    Compute C
    """
    results = dict()
    for i in range(num_groups):
        print("Executing group:", i)
        print("Evaluating:", groups[i])
        results[i] = dict()
        EC_cp = []
        c = []
        nonconformity_list = []
        for _ in range(num_test_trials):
            # Draw calibration data
            region_locations = [generate_region_location() for _ in range(groups[i]["num_calib"])]
            sensor_locations = [[generate_sensor_ouput(region_locations[n_c][n_o], sensor_noise) for n_o in range(num_region)] for n_c in range(groups[i]["num_calib"])]

            # Perform conformal prediction
            nonconformity = []
            for n_c in range(groups[i]["num_calib"]):
                nonconformity.append(max(math.sqrt((sensor_locations[n_c][n_o][0] - region_locations[n_c][n_o][0])**2 + (sensor_locations[n_c][n_o][1] - region_locations[n_c][n_o][1])**2) for n_o in range(num_region)))
            nonconformity.append(float("inf"))
            nonconformity.sort()
            p = int(np.ceil((groups[i]["num_calib"] + 1) * (1 - delta)))
            c.append(nonconformity[p - 1])
            nonconformity_list.append(nonconformity)
            # test results
            test_locations = [generate_region_location() for _ in range(num_test_samples)]
            test_sensor_locations = [[generate_sensor_ouput(test_locations[n_t][n_o], sensor_noise) for n_o in range(num_region)] for n_t in range(num_test_samples)]
            num_success = 0
            for n_c in range(num_test_samples):
                if max(math.sqrt((test_locations[n_c][n_o][0] - test_sensor_locations[n_c][n_o][0])**2 + (test_locations[n_c][n_o][1] - test_sensor_locations[n_c][n_o][1])**2) for n_o in range(num_region)) <= c[-1]:
                    num_success += 1
            EC_cp.append(num_success / num_test_samples)

        results[i]["EC_cp"] = EC_cp
        results[i]["c"] = c
        results[i]["nonconformity_list"] = nonconformity_list

    print("Saving data.")
    for i in range(num_groups):
        with open("results/example_1_num_calib=" + str(groups[i]["num_calib"]) + ".json", "w") as f:
            json.dump(results[i], f)



def control_cp():
    """
    Control with the obtained C
    """
    results = dict()
    for i in range(num_groups):
        results[i] = dict()
        with open("results/example_1_num_calib=" + str(groups[i]["num_calib"]) + ".json", "r") as file:
            results[i] = json.load(file)

    for i in range(num_groups):
        print("Executing group:", i)
        print("Evaluating:", groups[i])
        EC_control = []
        alldata_trajectory_x = []
        alldata_trajectory_y = []
        alldata_region_location_control = []
        alldata_sensor_location_control = []
        for trial_num in range(num_test_trials):
            print("Executing trial:", trial_num)
            trajectory_x = []
            trajectory_y = []
            region_location_control = []
            sensor_location_control = []
            success_count_controller = 0
            feasible_count_controller = 0
            for _ in range(num_test_samples):
                obstacle_location = generate_region_location() 
                sensor_location = [generate_sensor_ouput(obstacle_location[n_o], sensor_noise) for n_o in range(num_region)] 
                model = Model("model")
                model.setRealParam("limits/time", 100)
                # Initialize the variables and encode the system model.
                x, u = {}, {}
                for t in range(T+1):
                    for j in range(4):
                        x[t, j] = model.addVar(lb=None, ub=None, vtype="C", name="x(%s, %s)" % (t, j))
                for t in range(T):
                    for j in range(2):
                        u[t, j] = model.addVar(lb=None, ub=None, vtype="C", name="u(%s, %s)" % (t, j))
                for t in range(T):
                    for j in range(2):
                        model.addCons(u[t, j] >= -1)
                        model.addCons(u[t, j] <= 1)
                for t in range(T + 1):
                    if t == 0:
                        for j in range(4):
                            model.addCons(x[t, j] == 0)
                    else:
                        model.addCons(x[t, 0] == x[t-1, 0] + 0.5*x[t-1, 1] + 0.125*u[t-1, 0])
                        model.addCons(x[t, 1] == x[t-1, 1] + 0.5*u[t-1, 0])
                        model.addCons(x[t, 2] == x[t-1, 2] + 0.5*x[t-1, 3] + 0.125*u[t-1, 1])
                        model.addCons(x[t, 3] == x[t-1, 3] + 0.5*u[t-1, 1])
                # Encode the constraint from conformal prediction.
                # reaching final region
                model.addCons((x[T, 0] - final_region[0])**2 + (x[T, 2] - final_region[1])**2 <= final_distance**2)   
                # reaching uncertain regions
                for n_r in range(num_region):
                    model.addCons((x[time_point[n_r], 0] - sensor_location[n_r][0])**2 + (x[time_point[n_r], 2] - sensor_location[n_r][1])**2 <= (region_distance - results[i]["c"][trial_num])**2)

                # Set objective.
                objective = model.addVar(lb=None, ub=None, vtype="C", name="obj")
                model.addCons(0.4*sum(u[t, 0]**2 + u[t, 1]**2 for t in range(T-1)) + 0.6*((x[T, 0] - final_region[0])**2 + (x[T, 2] - final_region[1])**2) <= objective)
                model.setObjective(objective, "minimize")
                # optimization
                model.hideOutput()
                model.optimize()
                if model.getStatus() == "optimal":
                    sol = model.getBestSol()
                    x_opt1 = []
                    x_opt2 = []
                    for t in range(T+1):
                        x_opt1.append(sol[x[t, 0]])
                        x_opt2.append(sol[x[t, 2]])
                        
                    success_count_controller += is_successful_trajectory(x_opt1, x_opt2, obstacle_location, num_region, region_distance)
                    feasible_count_controller += 1
                    trajectory_x.append(x_opt1)
                    trajectory_y.append(x_opt2)
                    region_location_control.append(obstacle_location)
                    sensor_location_control.append(sensor_location)
                else:
                    print("infeasible")

            EC_control.append(success_count_controller / feasible_count_controller)
            print("EC_control:", success_count_controller / feasible_count_controller)
            alldata_trajectory_x.append(trajectory_x)
            alldata_trajectory_y.append(trajectory_y)
            alldata_region_location_control.append(region_location_control)
            alldata_sensor_location_control.append(sensor_location_control)
        
        results[i]["obstacle_location_control"] = alldata_region_location_control
        results[i]["sensor_location_control"] = alldata_sensor_location_control
        results[i]["EC_control"] = EC_control
        results[i]["trajectory_x"] = alldata_trajectory_x
        results[i]["trajectory_y"] = alldata_trajectory_y

    print("Saving data.")
    for i in range(num_groups):
        with open("results/example_1_num_calib=" + str(groups[i]["num_calib"]) + ".json", "w") as f:
            json.dump(results[i], f)


def main():
    cp()
    control_cp()


if __name__ == "__main__":
    main()