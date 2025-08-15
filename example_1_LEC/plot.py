import json
from parameters import *
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as patches
import tensorflow as tf

font_size = 28
label_size = 24
legend_size = 24

model = tf.keras.models.load_model("data and figure/trained_model.h5")


def plot_CEC(results, num_bins):
    catagory = "CEC"
    min_value = min(min(results[i][catagory]) for i in range(num_groups))
    max_value = max(max(results[i][catagory]) for i in range(num_groups))
    x = [None]*num_groups
    y = [None]*num_groups
    
    plt.figure(figsize=(8.7, 7.6))
    for i in range(num_groups):
        y[i], x[i] = np.histogram(results[i][catagory], bins=np.arange(min_value, max_value + (max_value - min_value) / num_bins, (max_value - min_value) / num_bins))
        sns.lineplot(x=x[i][:-1], y=y[i])
        plt.fill_between(x=x[i][:-1], y1=y[i], y2=0, alpha=0.3, label = "$K$ = " + str(groups[i]["num_calib"]))

    plt.legend(fontsize = legend_size)
    plt.tick_params("x", labelsize=label_size)
    plt.tick_params("y", labelsize=label_size)
    plt.ylabel("Frequency", fontsize = font_size)
    plt.xlabel(f"$CEC_n$", fontsize = font_size)
    plt.tight_layout()
    plt.savefig("data and figure/example1_CEC.pdf")

def plot_C(results, num_bins):
    catagory = "c"
    min_value = min(min(results[i][catagory]) for i in range(num_groups))
    max_value = max(max(results[i][catagory]) for i in range(num_groups))
    x = [None]*num_groups
    y = [None]*num_groups
    
    plt.figure(figsize=(8.7, 7.6))
    for i in range(num_groups):
        y[i], x[i] = np.histogram(results[i][catagory], bins=np.arange(min_value, max_value + (max_value - min_value) / num_bins, (max_value - min_value) / num_bins))
        sns.lineplot(x=x[i][:-1], y=y[i])
        plt.fill_between(x=x[i][:-1], y1=y[i], y2=0, alpha=0.3, label = "$K$ = " + str(groups[i]["num_calib"]))

    plt.legend(fontsize = legend_size)
    plt.tick_params("x", labelsize=label_size)
    plt.tick_params("y", labelsize=label_size)
    plt.ylabel("Frequency", fontsize = font_size)
    plt.xlabel(f"$C_n$", fontsize = font_size)
    plt.tight_layout()
    plt.savefig("data and figure/example1_C.pdf")

def illustration():
    inputs = np.array([generate_input() for _ in range(1000)])
    y_pred_list = model.predict(inputs)

    plt.figure(figsize=(8.7, 7.6))
    ax = plt.gca()
    plt.scatter(y_pred_list[:, 0], y_pred_list[:, 1], color='blue', label='Output', alpha=0.3)
    circle = plt.Circle((center_x, center_y), radius, color='blue', fill=False, label='Safe region')
    ax.add_patch(circle)

    plt.tick_params("x", labelsize=label_size)
    plt.tick_params("y", labelsize=label_size)
    plt.ylabel("$p^x_{10}$", fontsize = font_size)
    plt.xlabel(f"$p^y_{10}$", fontsize = font_size)
    
    plt.legend(fontsize = 20)
    plt.axis('equal')
    # plt.xlim([6.2, 13.5])
    # plt.ylim([5, 15])
    plt.tight_layout()
    plt.savefig("data and figure/example1_illstration.pdf")


def main():
    results = dict()
    for i in range(num_groups):
        results[i] = dict()
        with open("data and figure/example_1_num_calib=" + str(groups[i]["num_calib"]) + ".json", "r") as file:
            results[i] = json.load(file)
    
            
    plot_CEC(results, 18)
    plot_C(results, 18)
    illustration()



if __name__ == "__main__":
    main()