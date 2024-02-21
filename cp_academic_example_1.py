"""
Author: Yiqi Zhao

In this file, we implement a simple controller with a single integrator dynamics for obstacle avoidance in 2D Euclidean space with an imperfect sensor.

The dynamics is given by the difference equation x_(tau + 1) = x(tau) + u (with a sampling period of 1).
Initially, the robot is located at the origin, and the scope of u is 0.1 < u_x < 0.2 and 0.1 < u_y < 0.2. The sensor output follows a normal distribution
with a mean of the obstacle location and a standard deviation of 0.1 in both dimensions.

References:
    https://web.casadi.org/blog/opti/
    https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/
"""

import numpy as np
import matplotlib.pyplot as plt
import math
import casadi as ca
from pyscipopt import Model
import json
import os
from matplotlib.lines import Line2D
from parameters import *

np.random.seed(12)

def generate_obstacale_location():
    """
    This function generates the location of an obstacle.
    :return: the location of an obstacle.
    """
    return [np.random.uniform(2, 3), np.random.uniform(1.5, 3.5)]


def generate_sensor_ouput(obstacle_location, sensor_noise):
    """
    This function generates the sensor output given the obstacle location.
    :param obstacle_location: The location of the obstacle.
    :param sensor_noise: The noise of the sensor output location in terms of the standard deviation for the normal distribution.
    :return: The sensor output location.
    """
    return [np.random.laplace(obstacle_location[0], sensor_noise), np.random.laplace(obstacle_location[1], sensor_noise)]

def is_successful_trajectory(trajectory_x, trajectory_y, obstacle_location, num_obs, distance_threshold):
    """
    This function checks whether a trajectory is successful or not.
    :param trajectory_x: The x coordinates of the trajectory.
    :param trajectory_y: The y coordinates of the trajectory.
    :param obstacle_location1: The location of the first obstacle.
    :param obstacle_location2: The location of the second obstacle.
    :param distance_threshold: The distance threshold for the obstacle avoidance.
    :return: True if the trajectory is successful, and False otherwise.
    """
    for t in range(len(trajectory_x)):
        if min(math.sqrt((trajectory_x[t] - obstacle_location[n_o][0])**2 + (trajectory_y[t] - obstacle_location[n_o][1])**2) - distance_threshold for n_o in range(num_obs)) < 0:
            print("Oops! It collides with obstacles!")
            return False
    return True


def cp():
    results = dict()
    for i in range(num_groups):
        print("Executing group:", i)
        print("Evaluating:", groups[i])
        results[i] = dict()
        EC_cp = []
        c = []
        for _ in range(num_test_trials):
            # Draw calibration data
            obstacle_locations = [[generate_obstacale_location() for _ in range(num_obs)] for _ in range(groups[i]["num_calib"])]
            sensor_locations = [[generate_sensor_ouput(obstacle_locations[n_c][n_o], sensor_noise) for n_o in range(num_obs)] for n_c in range(groups[i]["num_calib"])]
            # Perform conformal prediction
            nonconformity_list = []
            for n_c in range(groups[i]["num_calib"]):
                nonconformity_list.append(max(math.sqrt((sensor_locations[n_c][n_o][0] - obstacle_locations[n_c][n_o][0])**2 + (sensor_locations[n_c][n_o][1] - obstacle_locations[n_c][n_o][1])**2) for n_o in range(num_obs)))
            nonconformity_list.append(float("inf"))
            nonconformity_list.sort()
            p = int(np.ceil((groups[i]["num_calib"] + 1) * (1 - delta)))
            c.append(nonconformity_list[p - 1])
            # test results
            test_obstacle_locations = [[generate_obstacale_location() for _ in range(num_obs)] for _ in range(num_test_samples)]
            test_sensor_locations = [[generate_sensor_ouput(test_obstacle_locations[i][n_o], sensor_noise) for n_o in range(num_obs)] for i in range(num_test_samples)]
            num_success = 0
            for n_c in range(num_test_samples):
                if max(math.sqrt((test_obstacle_locations[n_c][n_o][0] - test_sensor_locations[n_c][n_o][0])**2 + (test_obstacle_locations[n_c][n_o][1] - test_sensor_locations[n_c][n_o][1])**2) for n_o in range(num_obs)) <= c[-1]:
                    num_success += 1
            EC_cp.append(num_success / num_test_samples)

        results[i]["EC_cp"] = EC_cp
        results[i]["c"] = c

    print("Saving data.")
    for i in range(num_groups):
        with open("results/example_1_num_calib=" + str(groups[i]["num_calib"]) + ".json", "w") as f:
            json.dump(results[i], f)

def control_cp():
    results = dict()
    for i in range(num_groups):
        results[i] = dict()
        with open("results/example_1_num_calib=" + str(groups[i]["num_calib"]) + ".json", "r") as file:
            results[i] = json.load(file)

    for i in range(num_groups):
    # for i in range(1):
        print("Executing group:", i)
        print("Evaluating:", groups[i])
        EC_control = []
        trajectory_x = []
        trajectory_y = []
        obstacle_location_control = []
        sensor_location_control = []
        # obstacle_location_control = [[generate_obstacale_location() for _ in range(num_obs)] for _ in range(num_test_trials)]
        # sensor_location_control = [[generate_sensor_ouput(obstacle_location_control[trial_num][n_o], sensor_noise) for n_o in range(num_obs)] for trial_num in range(num_test_trials)]
        success_count_controller = 0
        feasible_count_controller = 0
        for trial_num in range(2):
            print("Executing trial:", trial_num)
            obstacle_location = [generate_obstacale_location() for _ in range(num_obs)] 
            sensor_location = [generate_sensor_ouput(obstacle_location[n_o], sensor_noise) for n_o in range(num_obs)] 
            model = Model("model")
            model.setRealParam("limits/time", 100)
            # Initialize the variables.
            x, u = {}, {}
            for t in range(T+1):
                for j in range(2):
                    x[t, j] = model.addVar(lb=None, ub=None, vtype="C", name="x(%s, %s)" % (t, j))
            for t in range(T):
                for j in range(2):
                    u[t, j] = model.addVar(lb=None, ub=None, vtype="C", name="u(%s, %s)" % (t, j))
            for t in range(T):
                for j in range(2):
                    model.addCons(u[t, j] >= 0)
                    model.addCons(u[t, j] <= 1.5)
            for t in range(T + 1):
                if t == 0:
                    model.addCons(x[t, 0] == 0)
                    model.addCons(x[t, 1] == 0)
                else:
                    model.addCons(x[t, 0] == x[t-1, 0] + u[t-1, 0])
                    model.addCons(x[t, 1] == x[t-1, 1] + u[t-1, 1])
            # Encode the constraint from conformal prediction.
            # circle obstacles
            for n_o in range(num_obs):
                for t in range(time_point[0], time_point[1]):
                # for t in range(T+1):
                    model.addCons((x[t, 0] - sensor_location[n_o][0])**2 + (x[t, 1] - sensor_location[n_o][1])**2 >= (results[i]["c"][trial_num] + distance_threshold)**2)
            
            # square obstacles
            # z = {}
            # for n_o in range(num_obs):
            #     for t in range(time_point[0], 10):
            #         for n_b in range(4):
            #             z[t, n_o, n_b] = model.addVar(lb=None, ub=None, vtype="B", name="x(%s, %s, %s)" % (t, n_o, n_b))
            # for n_o in range(num_obs):
            #     for t in range(time_point[0], 10):
            #         model.addCons(x[t, 0] - sensor_location[n_o][0] - (distance_threshold + results[i]["c"][trial_num]) >=  - M*(1-z[t, n_o, 0]))
            #         model.addCons(sensor_location[n_o][0] - (distance_threshold + results[i]["c"][trial_num]) - x[t, 0] >=  - M*(1-z[t, n_o, 1]))
            #         model.addCons(x[t, 1] - sensor_location[n_o][1] - (distance_threshold + results[i]["c"][trial_num]) >=  - M*(1-z[t, n_o, 2]))
            #         model.addCons(sensor_location[n_o][1] - (distance_threshold + results[i]["c"][trial_num]) - x[t, 1] >=  - M*(1-z[t, n_o, 3]))
            #         model.addCons(sum(z[t, n_o, n_b] for n_b in range(4)) >= 1)


            for t_p in range(len(time_point)):
                model.addCons((x[time_point[t_p], 0] - x_center[t_p])**2 + (x[time_point[t_p], 1] - y_center[t_p])**2 <= radius**2)
            # Set objective.
            objective = model.addVar(lb=None, ub=None, vtype="C", name="obj")
            model.addCons(sum((u[t+1, 0] - u[t, 0])**2 + (u[t+1, 1] - u[t, 1])**2 for t in range(T-1)) + sum((x[time_point[t_p], 0] - x_center[t_p])**2 + (x[time_point[t_p], 1] - y_center[t_p])**2 for t_p in range(len(time_point))) <= objective)
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
                    x_opt2.append(sol[x[t, 1]])
                    
                success_count_controller += is_successful_trajectory(x_opt1, x_opt2, obstacle_location, num_obs, distance_threshold)
                feasible_count_controller += 1
                trajectory_x.append(x_opt1)
                trajectory_y.append(x_opt2)
                obstacle_location_control.append(obstacle_location)
                sensor_location_control.append(sensor_location)
            else:
                print("infeasible")

        EC_control.append(success_count_controller / feasible_count_controller)
        print("EC_control:", success_count_controller / feasible_count_controller)
        
        results[i]["obstacle_location_control"] = obstacle_location_control
        results[i]["sensor_location_control"] = sensor_location_control
        results[i]["EC_control"] = EC_control
        results[i]["trajectory_x"] = trajectory_x
        results[i]["trajectory_y"] = trajectory_y

    # print("Saving data.")
    # for i in range(num_groups):
    #     with open("results/example_1_num_calib=" + str(groups[i]["num_calib"]) + ".json", "w") as f:
    #         json.dump(results[i], f)

            


def main():
    # cp()
    control_cp()

    

if __name__ == "__main__":
    main()