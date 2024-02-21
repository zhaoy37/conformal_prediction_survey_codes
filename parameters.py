groups = [{"num_calib": 100},
            {"num_calib": 500},
            {"num_calib": 1000}]
num_groups = len(groups)

num_test_samples = 1000 # The number of test samples.
num_test_trials = 300 # The number of test trials.
T = 20 # The time horizon.
sensor_noise = 0.02 # The noise of the sensor output location in terms of the standard deviation for the normal distribution.
distance_threshold = 0.2 # The distance threshold for the obstacle avoidance.
delta = 0.05 # The expected miscoverage rate.
num_obs = 3
time_point = [5, 15, T]
x_center = [2, 3, 5]
y_center = [0.5, 4.5, 5]
radius = 0.5


M = 1000