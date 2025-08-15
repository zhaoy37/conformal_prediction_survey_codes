import json
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


font_size = 28
label_size = 24
legend_size = 24
fig_size = (8.7, 7.6)
num_bins = 15


def main():
    # Plot example trajectories.
    with open("results/illustration_altitudes.json", "r") as f:
        illustration_altitudes = json.load(f)
    with open("results/illustration_velocities.json", "r") as f:
        illustration_velocities = json.load(f)
    with open("results/pred_illu_altitudes.json", "r") as f:
        pred_illu_altitudes = json.load(f)
    with open("results/pred_illu_velocities.json", "r") as f:
        pred_illu_velocities = json.load(f)
    with open("results/current_time.json", "r") as f:
        current_time = json.load(f)
    def plot_trajectories_with_predictions(altitudes, velocities, pred_altitudes, pred_velocities, current_time, save_title=""):
        colors = ["r", "g", "b"]
        time_stamps = [i for i in range(len(altitudes[0]))]
        pred_time_stamps = [i for i in range(current_time + 1, len(altitudes[0]))]
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.7 * 2, 7.6))

        for i in range(len(altitudes)):
            ax1.plot(time_stamps, altitudes[i], color=colors[i])
            ax1.plot(pred_time_stamps, pred_altitudes[i][current_time + 1:], color=colors[i], linestyle="dashed")
        ax1.set_xlabel("Time (1/30 s)", fontsize = font_size)
        ax1.set_ylabel("Altitude (ft)", fontsize = font_size)
        ax1.tick_params("x", labelsize=label_size)
        ax1.tick_params("y", labelsize=label_size)

        for i in range(len(velocities)):
            ax2.plot(time_stamps, velocities[i], color=colors[i])
            ax2.plot(pred_time_stamps, pred_velocities[i][current_time + 1:], color=colors[i], linestyle="dashed")
        ax2.set_xlabel("Time (1/30 s)", fontsize = font_size)
        ax2.set_ylabel("Velocity (ft/s)", fontsize = font_size)
        ax2.tick_params("x", labelsize=label_size)
        ax2.tick_params("y", labelsize=label_size)
        plt.tight_layout()
        if save_title != "":
            plt.savefig("plots_survey_paper/" + save_title + ".pdf")
        plt.show()
    plot_trajectories_with_predictions(illustration_altitudes, illustration_velocities, pred_illu_altitudes,
                                       pred_illu_velocities, current_time, save_title="example_predictions_nominal")

    # Plot the histogram of nonconformity scores for the direct method.
    with open("results/direct_nonconformity_scores.json", "r") as f:
        direct_nonconformity_scores = json.load(f)
    with open("results/c_direct.json", "r") as f:
        c_direct = json.load(f)
    plt.figure(figsize=(8.7, 7.6))
    plt.hist(direct_nonconformity_scores[:-1], bins=20)
    plt.xlabel("Nonconformity Score", fontsize = font_size)
    plt.ylabel("Frequency", fontsize = font_size)
    plt.axvline(c_direct, label="c")
    plt.legend(fontsize=legend_size)
    plt.tick_params("x", labelsize=label_size)
    plt.tick_params("y", labelsize=label_size)
    plt.tight_layout()
    plt.savefig("plots_survey_paper/nonconformity_scores_direct.pdf")
    plt.show()

    # Plot the scatter plot of robustnesses for the direct methods.
    test_size = 200
    with open("results/direct_test_robustnesses.json", "r") as f:
        direct_test_robustnesses = json.load(f)
    with open("results/direct_test_lowerbound_robustnesses.json", "r") as f:
        direct_test_lowerbound_robustnesses = json.load(f)
    sorted_direct_test_robustnesses, sorted_direct_test_lowerbound_robustnesses = zip(
        *sorted(zip(direct_test_robustnesses, direct_test_lowerbound_robustnesses)))
    dot_sizes = [5 for j in range(test_size)]
    plt.figure(figsize=(8.7, 7.6))
    plt.scatter([j for j in range(test_size)], sorted_direct_test_robustnesses, s=dot_sizes, color="r",
                label="$\\rho^\phi(X, \\tau_0)$")
    plt.scatter([j for j in range(test_size)], sorted_direct_test_lowerbound_robustnesses, s=dot_sizes, color="g",
                label="$\\rho^*$")
    plt.xlabel("Sample (Sorted on $\\rho^\phi(X, \\tau_0)$)", fontsize = font_size)
    plt.ylabel("Robust Semantics Value", fontsize = font_size)
    plt.legend(fontsize=legend_size)
    plt.tick_params("x", labelsize=label_size)
    plt.tick_params("y", labelsize=label_size)
    plt.tight_layout()
    plt.savefig("plots_survey_paper/direct_robustnesses_scatter.pdf")
    plt.show()

    # Plot the coverages of the direct method.
    with open("results/direct_coverages.json", "r") as f:
            direct_coverages = json.load(f)
    plt.figure(figsize=(8.7, 7.6 * 1.03))
    min_value = min(direct_coverages)
    max_value = max(direct_coverages)
    y, x = np.histogram(direct_coverages, bins=np.arange(min_value, max_value + (max_value - min_value) / num_bins, (max_value - min_value) / num_bins))
    sns.lineplot(x=x[:-1], y=y)
    plt.fill_between(x=x[:-1], y1=y, y2=0, alpha=0.3)
    plt.xlabel("Coverage", fontsize = font_size)
    plt.ylabel("Frequency", fontsize = font_size)
    plt.tick_params("x", labelsize=label_size)
    plt.tick_params("y", labelsize=label_size)
    plt.tight_layout()
    plt.savefig("plots_survey_paper/direct_coverages.pdf")
    plt.show()

    # Plot the histogram of nonconformity scores for the indirect method.
    with open("results/indirect_nonconformity_scores.json", "r") as f:
        indirect_nonconformity_scores = json.load(f)
    with open("results/c_indirect.json", "r") as f:
        c_indirect = json.load(f)
    plt.figure(figsize=(8.7, 7.6))
    plt.hist(indirect_nonconformity_scores[:-1], bins=20)
    plt.xlabel("Nonconformity Score", fontsize = font_size)
    plt.ylabel("Frequency", fontsize = font_size)
    plt.axvline(c_indirect, label="c")
    plt.legend(fontsize=legend_size)
    plt.tight_layout()
    plt.tick_params("x", labelsize=label_size)
    plt.tick_params("y", labelsize=label_size)
    plt.savefig("plots_survey_paper/nonconformity_scores_indirect.pdf")
    plt.show()

    # Plot the scatter plot of robustnesses for the indirect methods.
    with open("results/indirect_test_robustnesses.json", "r") as f:
        indirect_test_robustnesses = json.load(f)
    with open("results/indirect_test_lowerbound_robustnesses.json", "r") as f:
        indirect_test_lowerbound_robustnesses = json.load(f)
    sorted_indirect_test_robustnesses, sorted_indirect_test_lowerbound_robustnesses = zip(
        *sorted(zip(indirect_test_robustnesses, indirect_test_lowerbound_robustnesses)))
    dot_sizes = [5 for j in range(test_size)]
    plt.figure(figsize=(8.7, 7.6))
    plt.scatter([j for j in range(test_size)], sorted_indirect_test_robustnesses, s=dot_sizes, color="r",
                label="$\\rho^\phi(X, \\tau_0)$")
    plt.scatter([j for j in range(test_size)], sorted_indirect_test_lowerbound_robustnesses, s=dot_sizes, color="g",
                label="$\\rho^*$")
    plt.xlabel("Sample (Sorted on $\\rho^\phi(X, \\tau_0)$)", fontsize = font_size)
    plt.ylabel("Robust Semantics Value", fontsize = font_size)
    plt.legend(fontsize=legend_size)
    plt.tick_params("x", labelsize=label_size)
    plt.tick_params("y", labelsize=label_size)
    plt.tight_layout()
    plt.savefig("plots_survey_paper/indirect_robustnesses_scatter.pdf")
    plt.show()

    # Plot the coverages of the indirect method.
    with open("results/indirect_coverages.json", "r") as f:
        indirect_coverages = json.load(f)
    plt.figure(figsize=(8.7, 7.6))
    min_value = min(indirect_coverages) - 0.05
    max_value = max(indirect_coverages) + 0.1
    y, x = np.histogram(indirect_coverages, bins=np.arange(min_value, max_value + (max_value - min_value) / num_bins,
                                                         (max_value - min_value) / num_bins))
    sns.lineplot(x=x[:-1], y=y)
    plt.fill_between(x=x[:-1], y1=y, y2=0, alpha=0.3)
    plt.xlabel("Coverage", fontsize = font_size)
    plt.ylabel("Frequency", fontsize = font_size)
    plt.tick_params("x", labelsize=label_size)
    plt.tick_params("y", labelsize=label_size)
    plt.tight_layout()
    plt.savefig("plots_survey_paper/indirect_coverages.pdf")
    plt.show()


if __name__ == "__main__":
    main()