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
import json
import os

np.random.seed(0)

def generate_obstacale_location():
    """
    This function generates the location of an obstacle.
    :return: the location of an obstacle.
    """
    return [np.random.uniform(2, 5), np.random.uniform(2, 5)]


def generate_sensor_ouput(obstacle_location, sensor_noise):
    """
    This function generates the sensor output given the obstacle location.
    :param obstacle_location: The location of the obstacle.
    :param sensor_noise: The noise of the sensor output location in terms of the standard deviation for the normal distribution.
    :return: The sensor output location.
    """
    return [np.random.normal(obstacle_location[0], sensor_noise), np.random.normal(obstacle_location[1], sensor_noise)]

def is_successful_trajectory(trajectory_x, trajectory_y, obstacle_location1, obstacle_location2, distance_threshold):
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
        if math.sqrt((trajectory_x[t] - obstacle_location1[0])**2 + (trajectory_y[t] - obstacle_location1[1])**2) < distance_threshold or \
                math.sqrt((trajectory_x[t] - obstacle_location2[0])**2 + (trajectory_y[t] - obstacle_location2[1])**2) < distance_threshold:
            return False
    return True


def main():
    # Switch to the results folder.
    os.chdir("results_cp_academic_example_1")

    # Define hyperparameters.
    num_calib_samples = 1000 # The number of calibration samples.
    num_test_samples = 1000 # The number of test samples.
    num_test_trials = 50 # The number of test trials.
    T = 100 # The time horizon.
    sensor_noise = 0.05 # The noise of the sensor output location in terms of the standard deviation for the normal distribution.
    distance_threshold = 0.1 # The distance threshold for the obstacle avoidance.
    delta = 0.1 # The expected miscoverage rate.

    success_rates_cp = []
    success_count_controller = 0
    for trial_num in range(num_test_trials):
        print("Trial Number:", trial_num)
        # Draw calibration data.
        obstacle_locations = [[generate_obstacale_location(), generate_obstacale_location()] for i in range(num_calib_samples)]
        sensor_locations = [[generate_sensor_ouput(obstacle_locations[i][0], sensor_noise), generate_sensor_ouput(obstacle_locations[i][1], sensor_noise)] for i in range(num_calib_samples)]

        # Perform conformal prediction.
        nonconformity_list = []
        for i in range(num_calib_samples):
            nonconformity_list.append(min(math.sqrt((sensor_locations[i][0][0] - obstacle_locations[i][0][0])**2 + (sensor_locations[i][0][1] - obstacle_locations[i][0][1])**2),
                                          math.sqrt((sensor_locations[i][1][0] - obstacle_locations[i][1][0])**2 + (sensor_locations[i][1][1] - obstacle_locations[i][1][1])**2)))
        nonconformity_list.append(float("inf"))
        nonconformity_list.sort()
        p = int(np.ceil((num_calib_samples + 1) * (1 - delta)))
        c = nonconformity_list[p - 1]
        print("Prediction region on Conformal Prediction:", c)

        plt.hist(nonconformity_list[:-1], bins=10)
        plt.axvline(x=c, color='r', linestyle='--', label="Prediction Region C")
        plt.legend()
        plt.title("Nonconformity Scores for Conformal Prediction at trial " + str(trial_num))
        plt.savefig("nonconformity_scores_trial_" + str(trial_num) + ".pdf")
        plt.show()

        test_obstacle_locations = [[generate_obstacale_location(), generate_obstacale_location()] for i in range(num_test_samples)]
        test_sensor_locations = [[generate_sensor_ouput(test_obstacle_locations[i][0], sensor_noise), generate_sensor_ouput(test_obstacle_locations[i][1], sensor_noise)] for i in range(num_test_samples)]
        num_success = 0
        for i in range(num_test_samples):
            if min(math.sqrt((test_sensor_locations[i][0][0] - test_obstacle_locations[i][0][0])**2 + (test_sensor_locations[i][0][1] - test_obstacle_locations[i][0][1])**2),
                    math.sqrt((test_sensor_locations[i][1][0] - test_obstacle_locations[i][1][0])**2 + (test_sensor_locations[i][1][1] - test_obstacle_locations[i][1][1])**2)) <= c:
                num_success += 1
        print("Success Rate for Conformal Prediction:", num_success / num_test_samples)
        success_rates_cp.append(num_success / num_test_samples)

        # Perform Control synthesis using casadi.
        # Use one sensor output.
        obstacle_location1 = generate_obstacale_location()
        obstacle_location2 = generate_obstacale_location()
        sensor_location1 = generate_sensor_ouput(obstacle_location1, sensor_noise)
        sensor_location2 = generate_sensor_ouput(obstacle_location2, sensor_noise)
        # Perform optimization.
        opti = ca.Opti()
        # Encode the dynamics.
        u_x = opti.variable()
        u_y = opti.variable()
        opti.subject_to(u_x - 0.01 >= 0.1)
        opti.subject_to(u_y - 0.01 >= 0.1)
        opti.subject_to(u_x + 0.01 <= 0.2)
        opti.subject_to(u_y + 0.01 <= 0.2)
        x = [[opti.variable(), opti.variable()] for i in range(T + 1)]
        for t in range(T + 1):
            if t == 0:
                opti.subject_to(x[t][0] == 0)
                opti.subject_to(x[t][1] == 0)
            else:
                opti.subject_to(x[t][0] == x[t - 1][0] + u_x)
                opti.subject_to(x[t][1] == x[t - 1][1] + u_y)
        # Encode the constraint from conformal prediction.
        for t in range(T):
            opti.subject_to(ca.sqrt((x[t][0] - sensor_location1[0])**2 + (x[t][1] - sensor_location1[1])**2) - distance_threshold >= c)
            opti.subject_to(ca.sqrt((x[t][0] - sensor_location2[0])**2 + (x[t][1] - sensor_location2[1])**2) - distance_threshold >= c)
        # Set objective.
        opti.minimize(u_x**2 + u_y**2)
        # Solve the optimization problem.
        solver_opts = {'ipopt': {'print_level': 0}}
        opti.solver('ipopt', solver_opts)
        solution = opti.solve()
        # Print the optimal value of u.
        optimal_u_x = solution.value(u_x)
        optimal_u_y = solution.value(u_y)
        print("The optimal value of u_x is:", optimal_u_x)
        print("The optimal value of u_y is:", optimal_u_y)
        trajectory_x = []
        trajectory_y = []
        for t in range(T + 1):
            if t == 0:
                trajectory_x.append(0)
                trajectory_y.append(0)
            else:
                trajectory_x.append(trajectory_x[-1] + optimal_u_x)
                trajectory_y.append(trajectory_y[-1] + optimal_u_y)
        success_count_controller += is_successful_trajectory(trajectory_x, trajectory_y, obstacle_location1, obstacle_location2, distance_threshold)
        print()

        # Plot the trajectory plot.
        plt.plot(trajectory_x[20:50], trajectory_y[20:50], label="Trajectory")
        plt.scatter(sensor_location1[0], sensor_location1[1], label="Sensor Estimated Location for Obstacle 1")
        plt.scatter(sensor_location2[0], sensor_location2[1], label="Sensor Estimated Location for Obstacle 2")
        plt.scatter(obstacle_location1[0], obstacle_location1[1], label="Obstacle Location 1")
        plt.scatter(obstacle_location2[0], obstacle_location2[1], label="Obstacle Location 2")
        plt.legend()
        plt.title(f"Robot Trajectory with the Synthesized Controller for Trial {trial_num} from t = 20 to t = 50", font = {'size': 10})
        plt.savefig(f"trajectory_trial_{trial_num}.pdf")
        plt.show()
        print()

    # Plot coverages.
    plt.hist(success_rates_cp, bins=10)
    plt.title("Coverage for Conformal Prediction")
    plt.xlabel("Coverage")
    plt.ylabel("Frequency")
    plt.savefig("coverage_cp.pdf")
    plt.show()

    print("Success rate of the controller", success_count_controller / num_test_trials)
    with open("controll_success_rate.json", "w") as outfile:
        outfile.write(str(success_count_controller / num_test_trials))

    with open("coverage_cp.json", "w") as outfile:
        json.dump(success_rates_cp, outfile)

if __name__ == "__main__":
    main()