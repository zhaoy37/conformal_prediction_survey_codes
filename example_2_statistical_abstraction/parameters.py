from scipy.stats import truncnorm
import numpy as np


calib_percent = 0.5
trace_for_alphas = 50
p_len = 20
delta = 0.05




num_test_trials = 500  # The number of test trials.


M = 100000 #big value for linearization of max constraint