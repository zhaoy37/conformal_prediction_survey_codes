import json
import numpy as np
import matplotlib.pyplot as plt

delta_theta = 0.2
delta_p = 4.5
delta = 0.05
J = 200
N_param = 500


def compute_robustness(trajectory):
    return min([min(delta_theta - abs(state[2]), delta_p - abs(state[0])) for state in trajectory])


def main():
    np.random.seed(7654321)
    # Load trajectories.
    with open("trajectories.json", "r") as f:
        trajectories = json.load(f)
    c_dict = dict()
    c_dict[100], c_dict[300], c_dict[500] = [], [], []
    coverage_dict = dict()
    conditional_coverage_dict = dict()
    for K in [100, 300, 500]:
        print("Working on K :=", K)
        correct_coverage = 0
        conditional_coverage_dict[K] = []
        for N in range(N_param):
            if N % 100 == 0:
                print("Working on index", N)
            # Sample K + 1 trajectories.
            np.random.shuffle(trajectories)
            # Use the first K as the calibration set.
            trajectories_calibration = trajectories[:K]
            # Use the K + 1 one as the test trajectory.
            test_trajectory = trajectories[K]
            # Use the K + 2 to K + J + 2 as the cond test set.
            cond_test_trajectories = trajectories[K + 1:K + J + 1]
            # Compute the nonconformity score.
            nonconformity_scores = [(0 - compute_robustness(trajectory)) for trajectory in trajectories_calibration]
            p = int(np.ceil((1 - delta) * (K + 1)))
            nonconformity_scores.sort()
            nonconformity_scores.append(float("inf"))
            c = nonconformity_scores[p - 1]
            if N == 0 and K == 500:
                # Save the nonconformity scores.
                with open("results/example_nonconformity_scores.json", "w") as f:
                    json.dump(nonconformity_scores[:-1], f)
                with open("results/example_c.json", "w") as f:
                    json.dump(c, f)
            c_dict[K].append(c)
            # Compute empirical coverage
            test_nonconformity = (0 - compute_robustness(test_trajectory))
            if test_nonconformity <= c:
                correct_coverage += 1
            # Compute conditional empirical coverage.
            correct_cond_coverage = 0
            for trajectory in cond_test_trajectories:
                test_nonconformity = (0 - compute_robustness(trajectory))
                if test_nonconformity <= c:
                    correct_cond_coverage += 1
            conditional_coverage_dict[K].append(correct_cond_coverage / J)
        coverage_dict[K] = correct_coverage / N_param

    # Save c_dict.
    with open("results/c_dict.json", "w") as f:
        json.dump(c_dict, f)

    # Save coverage_dict.
    with open("results/coverage_dict.json", "w") as f:
        json.dump(coverage_dict, f)

    # Save the conditional_coverage_dict.
    with open("results/conditional_coverage_dict.json", "w") as f:
        json.dump(conditional_coverage_dict, f)


if __name__ == "__main__":
    main()