import json
from parameters import *
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

num_bins = 20
font_size = 22
label_size = 17
legend_size = 18
title_position = -0.2


results = dict()
for i in range(num_groups):
    results[i] = dict()
    with open("results/example_1_num_calib=" + str(groups[i]["num_calib"]) + ".json", "r") as file:
        results[i] = json.load(file)


def plot_ec(catagory):
    min_value = min(min(results[i][catagory]) for i in range(num_groups))
    max_value = max(max(results[i][catagory]) for i in range(num_groups))
    x = [None]*num_groups
    y = [None]*num_groups
    
    plt.figure(figsize=(8, 6.2))
    for i in range(num_groups):
        y[i], x[i] = np.histogram(results[i][catagory], bins=np.arange(min_value, max_value + (max_value - min_value) / num_bins, (max_value - min_value) / num_bins))
        sns.lineplot(x=x[i][:-1], y=y[i])
        plt.fill_between(x=x[i][:-1], y1=y[i], y2=0, alpha=0.3, label = "$N_{calib}$ = " + str(groups[i]["num_calib"]))

    plt.legend(fontsize = legend_size)
    # plt.ylim(0, 30)
    plt.tick_params("x", labelsize=label_size)
    plt.tick_params("y", labelsize=label_size)
    plt.ylabel("Frequency", fontsize = font_size)
    plt.xlabel("$EC_{CP}$", fontsize = font_size)
    

    plt.savefig("results/example1_" + catagory + ".pdf")
    plt.show()


plot_ec("EC_cp")


