"""
Author: Xinyi Yu, Yiqi Zhao
"""

import json
from parameters import *
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42
import seaborn as sns
import matplotlib.patches as patches

font_size = 28
label_size = 24
legend_size = 24

def plot_ec(results, name, num_bins):
    min_value = min(min(results[i][name]) for i in range(num_groups))
    max_value = max(max(results[i][name]) for i in range(num_groups))
    x = [None]*num_groups
    y = [None]*num_groups
    
    plt.figure(figsize=(8.7, 7.6))
    for i in range(num_groups):
        y[i], x[i] = np.histogram(results[i][name], bins=np.arange(min_value, max_value + (max_value - min_value) / num_bins, (max_value - min_value) / num_bins))
        sns.lineplot(x=x[i][:-1], y=y[i])
        plt.fill_between(x=x[i][:-1], y1=y[i], y2=0, alpha=0.3, label = "$K$ = " + str(groups[i]["num_calib"]))

    plt.legend(fontsize = legend_size)
    plt.tick_params("x", labelsize=label_size)
    plt.tick_params("y", labelsize=label_size)
    plt.ylabel("Frequency", fontsize = font_size)
    if name == "CEC":
        plt.xlabel(f"$CEC_n$ for conformal prediction", fontsize = font_size)
    if name == "CEC_control":
        plt.xlabel(f"$CEC_n$ for control", fontsize = font_size)
    plt.tight_layout()
    plt.savefig("results/example0_" + name + ".pdf")


def plot_nonconformity(results, bin_width):
    nonconformity_list = results[2]["nonconformity_list"][0]
    plt.figure(figsize=(8.7, 7.6))
    nonconformity_list = nonconformity_list[:-1]
    bin_centers = np.arange(min(nonconformity_list)- bin_width / 2, max(nonconformity_list) + bin_width / 2, bin_width)
    plt.hist(nonconformity_list, bins=bin_centers, rwidth=1)
    c = results[2]["c"][0]
    plt.axvline(x = c, label = "$C$", color = "r")
    plt.ylabel("Frequency", fontsize=font_size)
    plt.xlabel("Score", fontsize=font_size)
    plt.tick_params(axis='x', labelsize = label_size)
    plt.tick_params(axis='y', labelsize = label_size)
    plt.legend(fontsize=legend_size)
    plt.tight_layout()
    plt.savefig("results/example0_nonconformity_score.pdf")

def plot_trajectories(results):
    group_list = [0, 1, 2]
    trail_list = [2, 2, 3]
    trajectory_x = [results[group_list[i]]["trajectory_x"][trail_list[i]][0] for i in range(3)]
    trajectory_y = [results[group_list[i]]["trajectory_y"][trail_list[i]][0] for i in range(3)]
    c = [results[group_list[i]]["c"][trail_list[i]] for i in range(3)]
    sensor_location_control = [results[group_list[i]]["sensor_location_control"][trail_list[i]][0] for i in range(3)]
    reaching_location_control = [results[group_list[i]]["reaching_location_control"][trail_list[i]][0] for i in range(3)]

    fig, ax = plt.subplots(1, 3, figsize=(15, 4.5))
    ax = ax.flatten()
    for i_p in range(3):
        ax[i_p].plot(trajectory_x[i_p][0:T+1], trajectory_y[i_p][0:T+1])
        for i in range(T+1):
            ax[i_p].scatter(trajectory_x[i_p][i], trajectory_y[i_p][i], color='blue', s=6)
        for i in range(num_region):
            ax[i_p].scatter(sensor_location_control[i_p][i][0], sensor_location_control[i_p][i][1], color='black', alpha=0.6, linewidth=0, label="$s_l$" if i == 0 else "")
            if i_p == 2 and i == num_region - 1:
                circle_1 = patches.Circle((reaching_location_control[i_p][i][0], reaching_location_control[i_p][i][1]), region_distance, color='red', fill=False, linestyle='dashed', linewidth=0.8, label = "radius $\epsilon$ ")
                circle_2 = patches.Circle((sensor_location_control[i_p][i][0], sensor_location_control[i_p][i][1]), region_distance - c[i_p], color='black', fill=False, linestyle='dashed', linewidth=0.8, label = "radius $\epsilon$ - C")
            else:
                circle_1 = patches.Circle((reaching_location_control[i_p][i][0], reaching_location_control[i_p][i][1]), region_distance, color='red', fill=False, linestyle='dashed', linewidth=0.8)
                circle_2 = patches.Circle((sensor_location_control[i_p][i][0], sensor_location_control[i_p][i][1]), region_distance - c[i_p], color='black', fill=False, linestyle='dashed', linewidth=0.8)
            ax[i_p].add_patch(circle_1)
            ax[i_p].add_patch(circle_2)
            ax[i_p].scatter(reaching_location_control[i_p][i][0], reaching_location_control[i_p][i][1], color='red', alpha=0.6, linewidth=0, label="$r_l$" if i == 0 else "")
        circle = patches.Circle((final_region[i], final_region[i]), final_distance, color='blue', fill=True, alpha=0.3, linewidth=0, label = "final area")
        ax[i_p].add_patch(circle)
        ax[i_p].axis('equal')
        ax[i_p].set_xlim(-0.5, 6) 
        ax[i_p].set_ylim(-0.5, 6)
        ax[i_p].tick_params("x", labelsize=18)
        ax[i_p].tick_params("y", labelsize=18)
    plt.legend(fontsize = 16)
    plt.tight_layout()
    plt.savefig(f"results/example0_trajectory_trials.pdf")




def main():
    results = dict()
    for i in range(num_groups):
        results[i] = dict()
        with open("results/example_0_num_calib=" + str(groups[i]["num_calib"]) + ".json", "r") as file:
            results[i] = json.load(file)
            
    plot_ec(results, "CEC", 18)
    plot_ec(results, "CEC_control", 15)
    plot_nonconformity(results, 0.008)
    plot_trajectories(results)


if __name__ == "__main__":
    main()