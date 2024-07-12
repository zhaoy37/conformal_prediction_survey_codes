import json
import numpy as np
import matplotlib.pyplot as plt

delta_theta = 0.2
delta_p = 4.5
delta = 0.05
J = 200


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
        correct_coverage = 0
        conditional_coverage_dict[K] = []
        for N in range(300):
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
                plt.hist(nonconformity_scores[:-1], bins=20, alpha=0.5, label='Nonconformity Scores')
                plt.axvline(c, label = 'C', color = 'r')
                plt.legend(loc='upper right')
                plt.xlabel('Nonconformity Scores')
                plt.ylabel('Frequency')
                plt.title('Histogram of Nonconformity Scores')
                plt.show()
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
        coverage_dict[K] = correct_coverage / 300

    # Plot the histogram of Cs.
    plt.hist(c_dict[100], bins=20, alpha=0.5, label='K=100')
    plt.hist(c_dict[300], bins=20, alpha=0.5, label='K=300')
    plt.hist(c_dict[500], bins=20, alpha=0.5, label='K=500')
    plt.legend(loc='upper right')
    plt.xlabel('C')
    plt.ylabel('Frequency')
    plt.title('Histogram of Cs')
    plt.show()

    for K in [100, 300, 500]:
        print(f"Empirical coverage for K = {K} is:", coverage_dict[K])

    # Plot the conditional coverages.
    for K in [100, 300, 500]:
        plt.hist(conditional_coverage_dict[K], bins=20, alpha=0.5, label=f'K={K}')
    plt.legend(loc='upper right')
    plt.xlabel('$CEC_n$')
    plt.ylabel('Frequency')
    plt.title('Histogram of Conditional Empirical Coverages')
    plt.show()


if __name__ == "__main__":
    main()