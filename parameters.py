"""
Author: Xinyi Yu, Yiqi Zhao
"""

groups = [{"num_calib": 100},
            {"num_calib": 500},
            {"num_calib": 1000}]
num_groups = len(groups)

num_test_samples = 500 # The number of test samples.
num_test_trials = 300  # The number of test trials.
T = 20                 # The time horizon.
sensor_noise = 0.025   # The noise of the sensor output location in terms of the standard deviation for the normal distribution.

delta = 0.05           # The expected miscoverage rate.
num_region = 2
time_point = [5, 15]
region_distance = 0.6

final_region = [5, 5]
final_distance = 0.2

M = 1000