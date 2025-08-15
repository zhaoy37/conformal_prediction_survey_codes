import matplotlib.pyplot as plt
import json
import math
import numpy as np
from parameters import *
import seaborn as sns
from matplotlib.ticker import FormatStrFormatter

font_size = 28
label_size = 24
legend_size = 24

def plot_circle(x, y, size, color="-b", label=None):  # pragma: no cover
    deg = list(range(0, 360, 5))
    deg.append(0)
    xl = [x + size * math.cos(np.deg2rad(d)) for d in deg]
    yl = [y + size * math.sin(np.deg2rad(d)) for d in deg]

    if label is None:
        plt.plot(xl, yl, color)
    else:
        plt.plot(xl, yl, color,label=label)

def ax_plot_circle(ax, i, x, y, size, color="-b", label=None):  # pragma: no cover
    deg = list(range(0, 360, 5))
    deg.append(0)
    xl = [x + size * math.cos(np.deg2rad(d)) for d in deg]
    yl = [y + size * math.sin(np.deg2rad(d)) for d in deg]

    if label is None:
        ax[i].plot(xl, yl, color)
    else:
        ax[i].plot(xl, yl, color,label=label)

def validationplots(x_val, y_val, x_hat, y_hat, Ds_cp_LCP, Ds_cp_union_bound, Ds_cp_normalization):
    for i in range(len(x_val[0])):

        errs_x = [x_hat[j][i] - x_val[j][i] for j in range(len(x_val))]
        errs_y = [y_hat[j][i] - y_val[j][i] for j in range(len(y_val))]

        plt.clf()
        plt.scatter(errs_x,errs_y,label="Prediction Errors")
        plt.xlabel("X Error",fontsize="16")
        plt.ylabel("Y Error",fontsize="16")
        plt.axis('equal')
        plot_circle(0,0,Ds_cp_LCP[i],'g-',label="SNSA-LCP")
        plot_circle(0,0,Ds_cp_union_bound[i],'r-',label="UB")
        plot_circle(0,0,Ds_cp_normalization[i],'b-',label="SNSA-CF")
        plt.legend(fontsize="16",loc="upper left")
        ax=plt.gca()
        ax.tick_params(axis='both', which='major', labelsize=12)
        plt.tight_layout()
        plt.savefig("images/validationPlots/step" + str(i) + ".pdf")
        plt.clf()

def PaperfigureValidationPlots_together(x_val, y_val, x_hat, y_hat, Ds_cp_LCP, Ds_cp_union_bound, Ds_cp_normalization):
    fig, ax = plt.subplots(1, 3, figsize=(12, 4))
    ax = ax.flatten()
    time_list = [3, 6, 9]
    for i in range(3):
        errs_x = [x_hat[j][time_list[i]] - x_val[j][time_list[i]] for j in range(len(x_val))]
        errs_y = [y_hat[j][time_list[i]] - y_val[j][time_list[i]] for j in range(len(y_val))]
        ax[i].scatter(errs_x,errs_y,label="Prediction Errors", s = 10)
        ax[i].axis('equal')
        ax_plot_circle(ax, i, 0,0,Ds_cp_LCP[time_list[i]],'b-',label="SNSA-LCP")
        ax_plot_circle(ax, i, 0,0,Ds_cp_union_bound[time_list[i]],'grey',label="UB")
        ax_plot_circle(ax, i, 0,0,Ds_cp_normalization[time_list[i]],'r-',label="SNSA-CF")
        if i == 0:
            ax[i].legend(fontsize = legend_size-10, loc = "lower left")
        ax[i].set_xlim(-0.48, 0.48) 
        ax[i].set_ylim(-0.48, 0.48)
        ax[i].set_title(f"{time_list[i]} step prediction error", fontsize = font_size-10)
        ax[i].tick_params(axis='x', labelsize=label_size-13)
        ax[i].tick_params(axis='y', labelsize=label_size-13)
        ax[i].set_yticks(np.arange(-0.4, 0.42, 0.2))
        ax[i].set_xticks(np.arange(-0.4, 0.42, 0.2))
    plt.tight_layout()
    plt.savefig(f"images/example2_validation_together.pdf")

def PaperfigureValidationPlots_separate(x_val, y_val, x_hat, y_hat, Ds_cp_LCP, Ds_cp_union_bound, Ds_cp_normalization):
    time_list = [3, 6, 9]
    for i in range(3):
        errs_x = [x_hat[j][time_list[i]] - x_val[j][time_list[i]] for j in range(len(x_val))]
        errs_y = [y_hat[j][time_list[i]] - y_val[j][time_list[i]] for j in range(len(y_val))]
        plt.clf()
        plt.figure(figsize=(8.7, 7.6))
        if i == 0:
            plt.scatter(errs_x,errs_y,label=r"$||e_{3} - \hat{e}_{3|0}||$", s = 10)
        elif i == 1:
            plt.scatter(errs_x,errs_y,label=r"$||e_{6} - \hat{e}_{6|0}||$", s = 10)
        else:
            plt.scatter(errs_x,errs_y,label=r"$||e_{9} - \hat{e}_{9|0}||$", s = 10)
        plt.axis('equal')
        plot_circle(0,0,Ds_cp_LCP[time_list[i]],'b-',label="SNSA-LCP")
        plot_circle(0,0,Ds_cp_union_bound[time_list[i]],'grey',label="UB")
        plot_circle(0,0,Ds_cp_normalization[time_list[i]],'r-',label="SNSA-CF")
        plt.legend(fontsize = legend_size, loc = "lower left")
        plt.xlim(-0.48, 0.48) 
        plt.ylim(-0.48, 0.48)
        plt.tick_params("x", labelsize=label_size)
        plt.tick_params("y", labelsize=label_size)
        plt.yticks(np.arange(-0.4, 0.42, 0.2))
        plt.xticks(np.arange(-0.4, 0.42, 0.2))
        plt.tight_layout()
        plt.savefig(f"images/example2_validation_separate_{time_list[i]}.pdf")


def TracePlots(all_x_valid, all_y_valid, all_x_l_valid, all_y_l_valid, Ds_cp_LCP, Ds_cp_union_bound, Ds_cp_normalization):
    for j in range(len(all_x_valid)):
        if j >= 5:
            continue
        x_vals = all_x_valid[j]
        y_vals = all_y_valid[j]
        x_hats = all_x_l_valid[j]
        y_hats = all_y_l_valid[j]

        plt.clf()
        ax = plt.gca()
        plt.figure(figsize=(8.7, 7.6))
        # plot positions
        plt.plot(x_vals,y_vals,'*',color='cyan',label="Actual locations")
        # plot predictions
        plt.plot(x_hats,y_hats,'b*',label="Predicted locations")

        # plot conformal regions
        for t in range(len(x_vals)):
            if t==0:
                leg_label_ours = "SNSA-LCP"
                leg_label_union = "UB"
                leg_label_nor = "SNSA-CF"
            else:
                leg_label_ours = "_nolegend_"
                leg_label_union = "_nolegend_"
                leg_label_nor = "_nolegend_"
            # LCP
            plot_circle(x_hats[t],y_hats[t],Ds_cp_LCP[t],'b-',label=leg_label_ours)
            # normalization
            plot_circle(x_hats[t],y_hats[t],Ds_cp_normalization[t],'r-',label=leg_label_nor)
            # union bound cp region
            plot_circle(x_hats[t],y_hats[t],Ds_cp_union_bound[t],'grey',label=leg_label_union)

        plt.axis("equal")
        plt.legend(fontsize = legend_size)
        plt.tick_params("x", labelsize=label_size)
        plt.tick_params("y", labelsize=label_size)
        plt.yticks(np.arange(-0.5, 1.4, 0.3))
        plt.ylabel("Y", fontsize = font_size)
        plt.xlabel("X", fontsize = font_size)
        plt.tight_layout()
        if j == 0:
            plt.savefig("images/example2_general.pdf")
        else:
            plt.savefig("images/traces/trace" + str(j) + ".pdf")
        plt.clf()


def plot_CEC(results, num_bins):
    catagory = "CEC"
    min_value = min(min(results[i][catagory]) for i in range(len(results)))
    max_value = max(max(results[i][catagory]) for i in range(len(results)))
    x = [None]*len(results)
    y = [None]*len(results)
    label = ["SNSA-LCP", "SNSA-CF", "UB"]
    
    plt.figure(figsize=(8.7, 7.6))
    for i in range(len(results)):
        y[i], x[i] = np.histogram(results[i][catagory], bins=np.arange(min_value, max_value + (max_value - min_value) / num_bins, (max_value - min_value) / num_bins))
        # plt.hist(x=x[i][:-1], bins=x[i], weights=y[i], alpha=0.7)
        sns.lineplot(x=x[i][:-1], y=y[i])
        plt.fill_between(x=x[i][:-1], y1=y[i], y2=0, alpha=0.3, label = label[i])

    plt.legend(fontsize = legend_size)
    plt.tick_params("x", labelsize=label_size)
    plt.tick_params("y", labelsize=label_size)
    plt.xlim(0.9, 1.0)
    plt.ylabel("Frequency", fontsize = font_size)
    plt.xlabel("Coverage", fontsize = font_size)
    plt.tight_layout()
    plt.savefig("images/example2_CEC.pdf")

def AverageAreaPlots(average_LCP, average_union, average_normalization):
    plt.clf()
    plt.figure(figsize=(8.7, 7.6))
    plt.scatter(range(p_len), average_LCP,c='b', label="SNSA-LCP")
    plt.scatter(range(p_len), average_union, c='grey', label="UB")
    plt.scatter(range(p_len), average_normalization, c='r', label="SNSA-CF")    
    plt.legend(fontsize = legend_size)
    plt.tick_params("x", labelsize=label_size)
    plt.tick_params("y", labelsize=label_size)
    plt.ylabel("Average CP Region Volume", fontsize = font_size)
    plt.xlabel(r"$\tau$", fontsize = font_size)
    plt.tight_layout()
    plt.savefig("images/example2_averagearea.pdf")

    

if __name__ == "__main__":
    with open("data_results/results_LCP.json") as f:
        result_LCP = json.load(f)
    with open("data_results/results_normalization.json") as f:
        result_normalization = json.load(f)
    with open("data_results/results_union.json") as f:
        result_union = json.load(f)
    
    with open("data_results/x_valid.json") as f:
        x_valid = json.load(f)
    with open("data_results/y_valid.json") as f:
        y_valid = json.load(f)
    with open("data_results/x_l_valid.json") as f:
        x_l_valid = json.load(f)
    with open("data_results/y_l_valid.json") as f:
        y_l_valid = json.load(f)

    
    # the result of the first test trial
    TracePlots(x_valid, y_valid, x_l_valid, y_l_valid, result_LCP["Ds_cp"][0], result_union["Ds_cp"][0], result_normalization["Ds_cp"][0])
    # PaperfigureValidationPlots_together(x_valid, y_valid, x_l_valid, y_l_valid, result_LCP["Ds_cp"][0], result_union["Ds_cp"][0], result_normalization["Ds_cp"][0])
    PaperfigureValidationPlots_separate(x_valid, y_valid, x_l_valid, y_l_valid, result_LCP["Ds_cp"][0], result_union["Ds_cp"][0], result_normalization["Ds_cp"][0])

    # the result for the 500 trials
    AverageAreaPlots(result_LCP["Ds_cp_average"], result_union["Ds_cp_average"], result_normalization["Ds_cp_average"])
    results = [result_LCP, result_normalization, result_union]
    plot_CEC(results, 20)




    

