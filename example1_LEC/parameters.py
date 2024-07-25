from scipy.stats import truncnorm
import numpy as np

np.random.seed(42)

groups = [{"num_calib": 100},
            {"num_calib": 500},
            {"num_calib": 1000}]
num_groups = len(groups)

num_test_samples = 500 # The number of test samples.
num_test_trials = 500  # The number of test trials.
T = 20                 # The time horizon.
sensor_noise = 0.025   # The noise of the sensor output location in terms of the standard deviation for the normal distribution.

delta = 0.05           # The expected miscoverage rate.
center_x = 13.5
center_y = 0.5
radius = 3

# truncated normal distribution
def truncated_normal(mean=1, std=0.1, lower=0, upper=2, size=2):
    a, b = (lower - mean) / std, (upper - mean) / std
    return truncnorm.rvs(a, b, loc=mean, scale=std, size=size)

def generate_input():
    init_position = np.random.rand(2).tolist() 
    velocity = truncated_normal(mean=1, std=0.1, lower=0, upper=2, size=2)
    turn_angle = np.random.randn() * 0.1
    input = np.concatenate((init_position, velocity, [turn_angle]))
    return input
