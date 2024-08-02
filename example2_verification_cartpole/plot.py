import json
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

N_param = 500
font_size = 28
label_size = 24
legend_size = 24
num_bins = 20

def main():
    with open("results/example_nonconformity_scores.json", "r") as f:
        nonconformity_scores = json.load(f)
    with open("results/example_c.json", "r") as f:
        c = json.load(f)
    plt.figure(figsize=(8.7, 7.6))
    plt.hist(nonconformity_scores[:-1], bins=20, label='Nonconformity Scores')
    plt.axvline(c, label='C', color='r')
    plt.legend(fontsize=legend_size)
    plt.tick_params("x", labelsize=label_size)
    plt.tick_params("y", labelsize=label_size)
    plt.xlabel('Nonconformity Scores', fontsize = font_size)
    plt.ylabel('Frequency', fontsize = font_size)
    plt.tight_layout()
    plt.savefig("example_2_histogram_nonconformities.pdf")

    # Plot the histogram of Cs.
    with open("results/c_dict.json", "r") as f:
        c_dict = json.load(f)
    min_value = min([min(c_dict[str(K)]) for K in [100, 300, 500]])
    max_value = max([max(c_dict[str(K)]) for K in [100, 300, 500]])
    x = [None] * 3
    y = [None] * 3
    plt.figure(figsize=(8.7, 7.6))
    Ks = [100, 300, 500]
    for i in range(3):
        y[i], x[i] = np.histogram(c_dict[str(Ks[i])], bins=np.arange(min_value, max_value + (max_value - min_value) / num_bins, (max_value - min_value) / num_bins))
        sns.lineplot(x=x[i][:-1], y=y[i])
        plt.fill_between(x=x[i][:-1], y1=y[i], y2=0, alpha=0.3, label="$K$ = " + str(Ks[i]))
    plt.legend(fontsize=legend_size)
    plt.tick_params("x", labelsize=label_size)
    plt.tick_params("y", labelsize=label_size)
    plt.ylabel("Frequency", fontsize=font_size)
    plt.xlabel('C', fontsize=font_size)
    plt.tight_layout()
    plt.savefig("example_2_histogram_cs.pdf")

    for K in [100, 300, 500]:
        average_c = sum(c_dict[str(K)]) / N_param
        print(f"Average C for K = {K} is", average_c)

    with open("results/coverage_dict.json", "r") as f:
        coverage_dict = json.load(f)
    for K in [100, 300, 500]:
        print(f"Empirical coverage for K = {K} is:", coverage_dict[str(K)])

    with open("results/conditional_coverage_dict.json", "r") as f:
        conditional_coverage_dict = json.load(f)
    # Plot the conditional coverages.
    min_value = min([min(conditional_coverage_dict[str(K)]) for K in [100, 300, 500]])
    max_value = max([max(conditional_coverage_dict[str(K)]) for K in [100, 300, 500]])
    x = [None] * 3
    y = [None] * 3
    plt.figure(figsize=(8.7, 7.6))
    Ks = [100, 300, 500]
    for i in range(3):
        y[i], x[i] = np.histogram(conditional_coverage_dict[str(Ks[i])], bins=np.arange(min_value, max_value + (max_value - min_value) / num_bins, (max_value - min_value) / num_bins))
        sns.lineplot(x=x[i][:-1], y=y[i])
        plt.fill_between(x=x[i][:-1], y1=y[i], y2=0, alpha=0.3, label="$K$ = " + str(Ks[i]))
    plt.legend(fontsize=legend_size)
    plt.tick_params("x", labelsize=label_size)
    plt.tick_params("y", labelsize=label_size)
    plt.ylabel("Frequency", fontsize=font_size)
    plt.xlabel(f"$CEC_n$", fontsize=font_size)
    plt.tight_layout()
    plt.savefig("example_2_histogram_conditional_coverages.pdf")


if __name__ == "__main__":
    main()