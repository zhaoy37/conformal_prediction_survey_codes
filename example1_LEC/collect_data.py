import numpy as np
import matplotlib.pyplot as plt
import json
from parameters import *

np.random.seed(42)


def generate_trajectory(num_samples):
    trajectories = []
    inputs = []
    outputs = []
    
    for _ in range(num_samples):
        init_position = np.random.rand(2).tolist() 
        velocity = truncated_normal(mean=1, std=0.1, lower=0, upper=2, size=2)
        turn_angle = np.random.randn() * 0.1
        trajectory = [init_position]
        current_position = init_position
        
        for t in range(9):
            # a slight turn at time step 4
            if t == 3:
                rotation_matrix = np.array([[np.cos(turn_angle), -np.sin(turn_angle)],
                                            [np.sin(turn_angle), np.cos(turn_angle)]])
                velocity = np.dot(rotation_matrix, velocity)
            current_position += velocity
            current_position += np.random.randn(2) * 0.03
            trajectory.append(current_position.tolist())
        trajectories.append(trajectory)
        inputs.append(np.concatenate((init_position, velocity, [turn_angle])).tolist() )
        outputs.append(trajectory[-1])
    return inputs, outputs, trajectories

num_samples = 10000
input, output, trajectories = generate_trajectory(num_samples)


with open("example1_LEC/data and figure/data_train_input.json", "w") as f:
    json.dump(input, f)
with open("example1_LEC/data and figure/data_train_output.json", "w") as f:
    json.dump(output, f)

# # plot figure to see the trajectories
# plt.figure(figsize=(8, 6))
# for i in range(5):
#     plt.plot(trajectories[i][:, 0], trajectories[i][:, 1], marker='o', label=f'Trajectory {i+1}')
# plt.title('Generated Trajectory')
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.legend()
# plt.grid(True)
# plt.show()



