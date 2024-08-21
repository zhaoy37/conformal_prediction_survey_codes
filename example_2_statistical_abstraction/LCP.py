

import numpy as np
# from gurobipy import *

import gurobipy as gp
from gurobipy import GRB

import time
import pickle
import random
import math
import matplotlib.pyplot as plt
from gurobipyTutorial import optimzeTimeAlphasKKT
import json
from parameters import *

PLOT_VALIDATION_TRACES = True
NUM_VALID_TO_PLOT = 100

def computeRValuesIndiv(x_vals,y_vals,x_hats,y_hats):

    R_vals = [ [math.sqrt((x_vals[i][j]-x_hats[i][j])**2 + (y_vals[i][j]-y_hats[i][j])**2) for j in range(len(x_vals[i]))]  for i in range(len(x_vals))  ]

    return R_vals



def computeCPCirlce(x_vals,y_vals,x_hats,y_hats,delta):

    R_vals = [ math.sqrt((x_vals[i]-x_hats[i])**2 + (y_vals[i]-y_hats[i])**2) for i in range(len(x_vals))]

    R_vals.sort()
    R_vals.append(max(R_vals))

    ind_to_ret = math.ceil(len(R_vals)*(1-delta))
    return(R_vals[ind_to_ret])



def computeCPFixedAlphas(x_vals,y_vals,x_hats,y_hats,alphas,delta):

    R_vals = [max([alphas[j]*math.sqrt((x_vals[i][j]-x_hats[i][j])**2 + (y_vals[i][j]-y_hats[i][j])**2) for j in range(len(x_vals[i])) ]) for i in range(len(x_vals))]
    
    R_vals.sort()
    R_vals.append(max(R_vals))

    ind_to_ret = math.ceil(len(R_vals)*(1-delta))
    return R_vals[ind_to_ret]



def computeCoverageRAndAlphas(x_vals,y_vals,x_hats,y_hats,alphas,D_cp):

    R_vals = [max([alphas[j]*math.sqrt((x_vals[i][j]-x_hats[i][j])**2 + (y_vals[i][j]-y_hats[i][j])**2) for j in range(len(x_vals[i])) ]) for i in range(len(x_vals))]

    num_points_within = sum(r <= D_cp for r in R_vals)
    coverage_pct = float(num_points_within)/len(R_vals)
    return coverage_pct


def computeCoverageCircle(x_vals,y_vals,x_hats,y_hats,Ds_cp):
    coverage_count = 0
    for i in range(len(x_vals)):
        temp = sum([1 if math.sqrt((x_vals[i][j]-x_hats[i][j])**2 + (y_vals[i][j]-y_hats[i][j])**2) > Ds_cp[j] else 0 for j in range(len(x_vals[i]))])
        if temp == 0:
            coverage_count += 1
        if i == 0:
            if temp == 0:
                one_time_count = 1
            else:
                one_time_count = 0
        
    coverage_pct = float(coverage_count)/len(x_vals)
    return coverage_pct, one_time_count


def data_preprocess(all_x, all_y, all_x_l, all_y_l, seed):
    random.seed(seed)

    ## create train/test split
    temp = list(zip(all_x, all_y, all_x_l,all_y_l))
    random.shuffle(temp)
    res1,res2,res3,res4 = zip(*temp)
    all_x,all_y,all_x_l,all_y_l = list(res1),list(res2),list(res3),list(res4)

    calib_ind = round(len(all_x)*calib_percent)


    all_x_calib = all_x[0:calib_ind]
    all_y_calib = all_y[0:calib_ind]
    all_x_l_calib = all_x_l[0:calib_ind]
    all_y_l_calib = all_y_l[0:calib_ind]

    x_calib_alphas = all_x_calib[0:trace_for_alphas]
    y_calib_alphas = all_y_calib[0:trace_for_alphas]
    x_l_calib_alphas = all_x_l_calib[0:trace_for_alphas]
    y_l_calib_alphas = all_y_l_calib[0:trace_for_alphas]

    x_calib_CP = all_x_calib[trace_for_alphas:]
    y_calib_CP = all_y_calib[trace_for_alphas:]
    x_l_calib_CP = all_x_l_calib[trace_for_alphas:]
    y_l_calib_CP = all_y_l_calib[trace_for_alphas:]

    x_valid = all_x[calib_ind:]
    y_valid = all_y[calib_ind:]
    x_l_valid = all_x_l[calib_ind:]
    y_l_valid = all_y_l[calib_ind:]


    return x_calib_alphas, y_calib_alphas, x_l_calib_alphas, y_l_calib_alphas, x_calib_CP, y_calib_CP, x_l_calib_CP, y_l_calib_CP, x_valid, y_valid, x_l_valid, y_l_valid


def CpAndValidation(all_x, all_y, all_x_l, all_y_l, seed, SAVE_DATA):
    
    x_calib_alphas, y_calib_alphas, x_l_calib_alphas, y_l_calib_alphas, x_calib_CP, y_calib_CP, x_l_calib_CP, y_l_calib_CP, x_valid, y_valid, x_l_valid, y_l_valid = data_preprocess(all_x, all_y, all_x_l, all_y_l, seed)

    ## compute R values of data
    R_vals_calib_alpha = computeRValuesIndiv(x_calib_alphas, y_calib_alphas, x_l_calib_alphas, y_l_calib_alphas)
    ## run optimziation to compute alpha
    time_start = time.time()
    m = optimzeTimeAlphasKKT(R_vals_calib_alpha, delta, M)
    time_end = time.time()
    time_cost = time_end - time_start
    alphas = []    
    for v in m.getVars():
        if "alphas" in v.varName:
            alphas.append(v.x)
    ## run CP using alpha values on remaining calibration data
    D_cp = computeCPFixedAlphas(x_calib_CP, y_calib_CP, x_l_calib_CP, y_l_calib_CP, alphas, delta)
    Ds_cp = []
    for i in range(len(alphas)):
        Ds_cp.append(D_cp/alphas[i])
    CEC, one_time_count = computeCoverageCircle(x_valid, y_valid, x_l_valid, y_l_valid, Ds_cp)

    if SAVE_DATA == 1:
        # save the data of one of the test trials
        with open("data_results/x_valid.json", "w") as f:
            json.dump(x_valid, f)
        with open("data_results/y_valid.json", "w") as f:
            json.dump(y_valid, f)
        with open("data_results/x_l_valid.json", "w") as f:
            json.dump(x_l_valid, f)
        with open("data_results/y_l_valid.json", "w") as f:
            json.dump(y_l_valid, f)

    return alphas, D_cp, Ds_cp, CEC, one_time_count, time_cost




if __name__ == "__main__":
    with open("data_original/all_x.json") as f:
        all_x = json.load(f)
    with open("data_original/all_y.json") as f:
        all_y = json.load(f)
    with open("data_original/all_x_l.json") as f:
        all_x_l = json.load(f)
    with open("data_original/all_y_l.json") as f:
        all_y_l = json.load(f)

    results = dict()
    CEC_list = []
    alphas_list = []
    D_cp_list = []
    Ds_cp_list = []
    time_list = []
    num_success_one_test = 0 # this is for equation (5)

    for i in range(num_test_trials):
        seed = i*2
        if i == 0:
            SAVE_DATA = 1
        else:
            SAVE_DATA = 0
        alphas, D_cp, Ds_cp, CEC, one_time_count, time_cost = CpAndValidation(all_x, all_y, all_x_l, all_y_l, seed, SAVE_DATA)
        alphas_list.append(alphas)
        D_cp_list.append(D_cp)
        Ds_cp_list.append(Ds_cp)
        CEC_list.append(CEC)
        time_list.append(time_cost)
        num_success_one_test += one_time_count
    
    EC = num_success_one_test / num_test_trials
    results["EC"] = EC
    results["CEC"] = CEC_list
    results["alphas"] = alphas_list
    results["D_cp"] = D_cp_list
    results["Ds_cp"] = Ds_cp_list
    results["time"] = time_list

    Ds_cp_average = []
    for i in range(p_len):
        Ds_cp_average.append(math.pi*(sum([Ds_cp_list[j][i] for j in range(num_test_trials)])/num_test_trials)**2)
    results["Ds_cp_average"] = Ds_cp_average
    results["time_average"] = sum(time_list)/num_test_trials

    print("Saving data.")
    with open("data_results/results_LCP.json", "w") as f:
        json.dump(results, f)



    


    