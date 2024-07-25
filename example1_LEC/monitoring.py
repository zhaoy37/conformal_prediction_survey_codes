import tensorflow as tf
import numpy as np
import json
import matplotlib.pyplot as plt
from parameters import *



model = tf.keras.models.load_model("example1_LEC/data and figure/trained_model.h5")


def cp():
    results = dict()
    for i in range(num_groups):
        print("Executing group:", i)
        print("Evaluating:", groups[i])
        results[i] = dict()
        CEC = []
        c = []
        nonconformity_list = []
        num_success_one_test = 0 # this is for equation (5)
        for _ in range(num_test_trials):
            inputs = np.array([generate_input() for _ in range(groups[i]["num_calib"])])
            y_pred_list = model.predict(inputs)
            # Perform conformal prediction
            nonconformity = []
            for j in range(groups[i]["num_calib"]):
                nonconformity.append((y_pred_list[j][0]-center_x) ** 2 + (y_pred_list[j][1]-center_y) ** 2 -radius ** 2)
            nonconformity.append(float("inf"))
            nonconformity.sort()
            p = int(np.ceil((groups[i]["num_calib"] + 1) * (1 - delta)))
            c.append(nonconformity[p - 1])
            nonconformity_list.append(nonconformity)
            
            # test results
            inputs = np.array([generate_input() for _ in range(num_test_samples)])
            y_pred_list = model.predict(inputs)
            num_success = 0
            for j in range(num_test_samples):
                if (y_pred_list[j][0]-center_x) ** 2 + (y_pred_list[j][1]-center_y) ** 2 -radius ** 2 <= c[-1]:
                    num_success += 1
                    if j == 0:
                        num_success_one_test += 1
            EC = num_success_one_test / num_test_trials
            CEC.append(num_success / num_test_samples)
        
        results[i]["EC"] = EC
        results[i]["CEC"] = CEC
        results[i]["c"] = c
        results[i]["nonconformity_list"] = nonconformity_list

    print("Saving data.")
    for i in range(num_groups):
        with open("example1_LEC/data and figure/example_1_num_calib=" + str(groups[i]["num_calib"]) + ".json", "w") as f:
            json.dump(results[i], f)

if __name__ == "__main__":
    cp()



