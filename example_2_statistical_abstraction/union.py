import json
import math
from parameters import *
import random

def computeCPCirlce(x_vals,y_vals,x_hats,y_hats,delta):
    R_vals = [ math.sqrt((x_vals[i]-x_hats[i])**2 + (y_vals[i]-y_hats[i])**2) for i in range(len(x_vals))]

    R_vals.sort()
    R_vals.append(max(R_vals))

    ind_to_ret = math.ceil(len(R_vals)*(1-delta))
    return(R_vals[ind_to_ret])


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

    x_calib_CP = all_x[0:calib_ind]
    y_calib_CP = all_y[0:calib_ind]
    x_l_calib_CP = all_x_l[0:calib_ind]
    y_l_calib_CP = all_y_l[0:calib_ind]

    x_valid = all_x[calib_ind:]
    y_valid = all_y[calib_ind:]
    x_l_valid = all_x_l[calib_ind:]
    y_l_valid = all_y_l[calib_ind:]

    return x_calib_CP, y_calib_CP, x_l_calib_CP, y_l_calib_CP, x_valid, y_valid, x_l_valid, y_l_valid


def CpAndValidation(all_x, all_y, all_x_l, all_y_l, seed):
    
    x_calib_CP, y_calib_CP, x_l_calib_CP, y_l_calib_CP, x_valid, y_valid, x_l_valid, y_l_valid = data_preprocess(all_x, all_y, all_x_l, all_y_l, seed)

    delta_union = delta/p_len
    Ds_cp = []
    
    for t in range(p_len):
        x_vals = [x_calib_CP[i][t] for i in range(len(x_calib_CP))]
        y_vals = [y_calib_CP[i][t] for i in range(len(x_calib_CP))]
        x_hats = [x_l_calib_CP[i][t] for i in range(len(x_calib_CP))]
        y_hats = [y_l_calib_CP[i][t] for i in range(len(x_calib_CP))]

        D_val = computeCPCirlce(x_vals,y_vals,x_hats,y_hats,delta_union)
        Ds_cp.append(D_val)

    CEC, one_time_count = computeCoverageCircle(x_valid, y_valid, x_l_valid, y_l_valid, Ds_cp)

    return Ds_cp, CEC, one_time_count


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
    Ds_cp_list = []
    num_success_one_test = 0 # this is for equation (5)

    for i in range(num_test_trials):
        seed = i*2
        Ds_cp, CEC, one_time_count = CpAndValidation(all_x, all_y, all_x_l, all_y_l, seed)
        Ds_cp_list.append(Ds_cp)
        CEC_list.append(CEC)
        num_success_one_test += one_time_count
    
    EC = num_success_one_test / num_test_trials
    results["EC"] = EC
    results["CEC"] = CEC_list
    results["Ds_cp"] = Ds_cp_list

    Ds_cp_average = []
    for i in range(p_len):
        Ds_cp_average.append(math.pi*(sum([Ds_cp_list[j][i] for j in range(num_test_trials)])/num_test_trials)**2)
    results["Ds_cp_average"] = Ds_cp_average

    print("Saving data.")
    with open("data_results/results_union.json", "w") as f:
        json.dump(results, f)









    