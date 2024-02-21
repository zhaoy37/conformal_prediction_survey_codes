import json
from parameters import *
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as patches

num_bins = 25
font_size = 22
label_size = 17
legend_size = 18
title_position = -0.2

results = dict()
for i in range(num_groups):
    results[i] = dict()
    with open("results/example_1_num_calib=" + str(groups[i]["num_calib"]) + ".json", "r") as file:
        results[i] = json.load(file)

group_list = [0, 1, 2]
trail_list = [13, 5, 8]
trajectory_x = [results[group_list[i]]["trajectory_x"][trail_list[i]] for i in range(3)]
trajectory_y = [results[group_list[i]]["trajectory_y"][trail_list[i]] for i in range(3)]
c = [results[group_list[i]]["c"][trail_list[i]] for i in range(3)]
sensor_location_control = [results[group_list[i]]["sensor_location_control"][trail_list[i]] for i in range(3)]
obstacle_location_control = [results[group_list[i]]["obstacle_location_control"][trail_list[i]] for i in range(3)]


fig, ax = plt.subplots(1, 3, figsize=(16, 4.5))
ax = ax.flatten()
for i_p in range(3):
    ax[i_p].plot(trajectory_x[i_p][0:T+1], trajectory_y[i_p][0:T+1])
    for i in range(T+1):
        ax[i_p].scatter(trajectory_x[i_p][i], trajectory_y[i_p][i], color='blue', s=6)
    for i in range(num_obs):
        ax[i_p].scatter(sensor_location_control[i_p][i][0], sensor_location_control[i_p][i][1], color='red', alpha=0.6, linewidth=0)
        if i_p == 2 and i == num_obs - 1:
            circle_1 = patches.Circle((sensor_location_control[i_p][i][0], sensor_location_control[i_p][i][1]), distance_threshold, color='red', fill=False, linestyle='dashed', linewidth=0.8, label = "radius $\epsilon$ regions")
            circle_2 = patches.Circle((sensor_location_control[i_p][i][0], sensor_location_control[i_p][i][1]), c[i_p] + distance_threshold, color='black', fill=False, linestyle='dashed', linewidth=0.8, label = "radius $c + \epsilon$ regions")
        else:
            circle_1 = patches.Circle((sensor_location_control[i_p][i][0], sensor_location_control[i_p][i][1]), distance_threshold, color='red', fill=False, linestyle='dashed', linewidth=0.8)
            circle_2 = patches.Circle((sensor_location_control[i_p][i][0], sensor_location_control[i_p][i][1]), c[i_p] + distance_threshold, color='black', fill=False, linestyle='dashed', linewidth=0.8)
        ax[i_p].add_patch(circle_1)
        ax[i_p].add_patch(circle_2)
        ax[i_p].scatter(obstacle_location_control[i_p][i][0], obstacle_location_control[i_p][i][1], color='blue', alpha=0.6, linewidth=0)
    for i in range(len(time_point)):
        if i_p == 2 and i == num_obs - 1:
            circle = patches.Circle((x_center[i], y_center[i]), radius, color='blue', fill=True, alpha=0.3, linewidth=0, label = "reaching requirement")
        else:
            circle = patches.Circle((x_center[i], y_center[i]), radius, color='blue', fill=True, alpha=0.3, linewidth=0)
        ax[i_p].add_patch(circle)

    ax[i_p].set_xlim(-0.5, 6)
    ax[i_p].set_ylim(-0.5, 6)
plt.legend()
plt.savefig(f"results/trajectory_trials.pdf")
plt.show()