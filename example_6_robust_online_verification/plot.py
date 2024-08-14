import json
import matplotlib.pyplot as plt


font_size = 28
label_size = 24
legend_size = 24
fig_size = (8.7, 7.6)


def main():
    with open("results/direct_nonconformity_scores.json", "r") as f:
        direct_nonconformity_scores = json.load(f)
    with open("results/c_direct.json", "r") as f:
        c_direct = json.load(f)
    with open("results/c_tilde_direct.json", "r") as f:
        c_tilde_direct = json.load(f)
    plt.figure(figsize=(8.7, 7.6))
    plt.hist(direct_nonconformity_scores[:-1], bins=20)
    plt.xlabel("Nonconformity Score", fontsize = font_size)
    plt.ylabel("Frequency", fontsize = font_size)
    plt.axvline(c_direct, label="$c$")
    plt.axvline(c_tilde_direct, label="$\\tilde{c}$")
    plt.legend(fontsize=legend_size)
    plt.tick_params("x", labelsize=label_size)
    plt.tick_params("y", labelsize=label_size)
    plt.tight_layout()
    plt.savefig("plots_survey_paper/nonconformity_scores_direct.pdf")
    plt.show()

    with open("results/direct_test_robustnesses.json", "r") as f:
        direct_test_robustnesses = json.load(f)
    with open("results/direct_test_lowerbound_robustnesses.json", "r") as f:
        direct_test_lowerbound_robustnesses = json.load(f)
    with open("results/robust_direct_test_lowerbound_robustnesses.json", "r") as f:
        robust_direct_test_lowerbound_robustnesses = json.load(f)
    test_size = 200
    sorted_direct_test_robustnesses, sorted_direct_test_lowerbound_robustnesses, sorted_robust_direct_test_lowerbound_robustnesses = zip(
        *sorted(zip(direct_test_robustnesses, direct_test_lowerbound_robustnesses,
                    robust_direct_test_lowerbound_robustnesses)))
    dot_sizes = [5 for j in range(test_size)]
    plt.figure(figsize=(8.7, 7.6))
    plt.scatter([j for j in range(test_size)], sorted_direct_test_robustnesses, s=dot_sizes, color="r",
                label="$\\rho^\phi(X, \\tau_0)$")
    plt.scatter([j for j in range(test_size)], sorted_direct_test_lowerbound_robustnesses, s=dot_sizes, color="g",
                label="$\\rho^*$ with Conformal Prediction")
    plt.scatter([j for j in range(test_size)], sorted_robust_direct_test_lowerbound_robustnesses, s=dot_sizes,
                color="b", label="$\\rho^*$ with Robust Conformal Prediction")
    plt.xlabel("Sample (Sorted on $\\rho^\phi(X, \\tau_0)$)", fontsize = font_size)
    plt.ylabel("Robust Semantics Value", fontsize = font_size)
    plt.legend(fontsize=legend_size)
    plt.tick_params("x", labelsize=label_size)
    plt.tick_params("y", labelsize=label_size)
    plt.tight_layout()
    plt.savefig("plots_survey_paper/direct_robustnesses_scatter.pdf")
    plt.show()

    with open("results/indirect_nonconformity_scores.json") as f:
        indirect_nonconformity_scores = json.load(f)
    with open("results/c_indirect.json") as f:
        c_indirect = json.load(f)
    with open("results/c_tilde_indirect.json") as f:
        c_tilde_indirect = json.load(f)
    plt.figure(figsize=(8.7, 7.6))
    plt.hist(indirect_nonconformity_scores[:-1], bins=20)
    plt.xlabel("Nonconformity Score", fontsize = font_size)
    plt.ylabel("Frequency", fontsize = font_size)
    plt.axvline(c_indirect, label="$c$")
    plt.axvline(c_tilde_indirect, label="$\\tilde{c}$")
    plt.legend(fontsize=legend_size)
    plt.tick_params("x", labelsize=label_size)
    plt.tick_params("y", labelsize=label_size)
    plt.tight_layout()
    plt.savefig("plots_survey_paper/nonconformity_scores_indirect.pdf")
    plt.show()

    with open("results/indirect_test_robustnesses.json") as f:
        indirect_test_robustnesses = json.load(f)
    with open("results/indirect_test_lowerbound_robustnesses.json") as f:
        indirect_test_lowerbound_robustnesses = json.load(f)
    with open("results/robust_indirect_test_lowerbound_robustnesses.json") as f:
        robust_indirect_test_lowerbound_robustnesses = json.load(f)
    sorted_indirect_test_robustnesses, sorted_indirect_test_lowerbound_robustnesses, sorted_robust_indirect_test_lowerbound_robustnesses = zip(
        *sorted(zip(indirect_test_robustnesses, indirect_test_lowerbound_robustnesses,
                    robust_indirect_test_lowerbound_robustnesses)))
    plt.figure(figsize=(8.7, 7.6))
    dot_sizes = [5 for j in range(test_size)]
    plt.scatter([j for j in range(test_size)], sorted_indirect_test_robustnesses, s=dot_sizes, color="r",
                label="$\\rho^\phi(X, \\tau_0)$")
    plt.scatter([j for j in range(test_size)], sorted_indirect_test_lowerbound_robustnesses, s=dot_sizes, color="g",
                label="$\\rho^*$ with Conformal Prediction")
    plt.scatter([j for j in range(test_size)], sorted_robust_indirect_test_lowerbound_robustnesses, s=dot_sizes,
                color="b", label="$\\rho^*$ with Robust Conformal Prediction")
    plt.xlabel("Sample (Sorted on $\\rho^\phi(X, \\tau_0)$)", fontsize = font_size)
    plt.ylabel("Robust Semantics Value", fontsize = font_size)
    plt.legend(fontsize=legend_size)
    plt.tick_params("x", labelsize=label_size)
    plt.tick_params("y", labelsize=label_size)
    plt.tight_layout()
    plt.savefig("plots_survey_paper/indirect_robustnesses_scatter.pdf")
    plt.show()

    with open("results/direct_coverages.json") as f:
        direct_coverages = json.load(f)
    with open("results/robust_direct_coverages.json") as f:
        robust_direct_coverages = json.load(f)
    plt.figure(figsize=(8.7, 7.6))
    plt.hist(direct_coverages, bins=20, label="non-robust direct method")
    plt.hist(robust_direct_coverages, bins=20, label="robust direct method")
    plt.xlabel("Coverage", fontsize = font_size)
    plt.ylabel("Frequency", fontsize = font_size)
    plt.legend(fontsize=legend_size)
    plt.tick_params("x", labelsize=label_size)
    plt.tick_params("y", labelsize=label_size)
    plt.tight_layout()
    plt.savefig("plots_survey_paper/direct_coverages.pdf")
    plt.show()

    with open("results/indirect_coverages.json") as f:
        indirect_coverages = json.load(f)
    with open("results/robust_indirect_coverages.json") as f:
        robust_indirect_coverages = json.load(f)
    plt.figure(figsize=(8.7, 7.6))
    plt.hist(indirect_coverages, bins=20, label="non-robust indirect method")
    plt.hist(robust_indirect_coverages, bins=20, label="robust indirect method")
    plt.xlabel("Coverage", fontsize = font_size)
    plt.ylabel("Frequency", fontsize = font_size)
    plt.legend(fontsize=legend_size)
    plt.tick_params("x", labelsize=label_size)
    plt.tick_params("y", labelsize=label_size)
    plt.tight_layout()
    plt.savefig("plots_survey_paper/indirect_coverages.pdf")
    plt.show()


if __name__ == "__main__":
    main()