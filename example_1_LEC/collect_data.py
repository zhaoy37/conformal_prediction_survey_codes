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
        # Initial conditions
        init_position = np.random.rand(2).tolist()
        velocity = truncated_normal(mean=1, std=0.1, lower=0, upper=2, size=2)
        angle = np.random.randn() * 0.1
        v = np.linalg.norm(velocity)  # constant forward velocity
        omega = 0  # constant angular velocity
        dt = 1  # time step

        # Initialize state
        x, y = init_position
        theta = angle

        # Store initial position in trajectory
        trajectory = [(x, y)]

        # Generate trajectory for 10 steps
        for _ in range(9):
            x += v * np.cos(theta) * dt
            y += v * np.sin(theta) * dt
            theta += omega * dt
            # Add some random noise to the position
            x += np.random.randn() * 0.01
            y += np.random.randn() * 0.01
            trajectory.append((x, y))

        trajectories.append(trajectory)
        inputs.append(np.concatenate((init_position, velocity, [angle])).tolist())
        outputs.append([x, y])
    
    return inputs, outputs, trajectories

num_samples = 10000
input, output, trajectories = generate_trajectory(num_samples)

with open("example1_LEC/data and figure/data_train_input.json", "w") as f:
    json.dump(input, f)
with open("example1_LEC/data and figure/data_train_output.json", "w") as f:
    json.dump(output, f)

# plot figure to see the trajectories
for i in range(20):
    x_trajectory, y_trajectory = zip(*trajectories[i])
    plt.plot(x_trajectory, y_trajectory, marker='o')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Unicycle Model Trajectory')
plt.grid(True)
plt.axis('equal')
plt.show()

