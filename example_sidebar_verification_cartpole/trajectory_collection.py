import gym
import torch
from dqn import DQN
import json
import numpy as np

num_trajectories = 1000


def collect_raw_trajectories():
    device = torch.device(
        "cuda" if torch.cuda.is_available() else
        "mps" if torch.backends.mps.is_available() else
        "cpu"
    )
    env = gym.make("CartPole-v1")
    state, info = env.reset()
    # Load Policy network
    n_observations = len(state)
    n_actions = env.action_space.n
    policy_net = DQN(n_observations, n_actions).to(device)
    policy_net.load_state_dict(torch.load("dqn.pth"))
    policy_net.eval()
    trajectories = []
    for i in range(num_trajectories):
        if i % 10 == 0:
            print(f"Generating Trajectory {i + 1}.")
        episode = []
        done = False
        state, info = env.reset()
        # Generate initial state.
        state = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
        episode.append(state.tolist()[0])
        while not done:
            with torch.no_grad():
                action = policy_net(state).max(1).indices.view(1, 1)
            observation, reward, terminated, truncated, _ = env.step(action.item())
            state = torch.tensor(observation, dtype=torch.float32, device=device).unsqueeze(0)
            done = terminated or truncated
            episode.append(state.tolist()[0])
        trajectories.append(episode)
    return trajectories


def main():
    raw_trajectories = collect_raw_trajectories()
    # Clip trajectories.
    clipping_index = min([len(episode) for episode in raw_trajectories])
    trajectories = [episode[:clipping_index] for episode in raw_trajectories]
    print("Trajectories clipped at index:", clipping_index)
    print("Shape of the trajectories:", np.shape(trajectories))
    # Save trajectories.
    with open("trajectories.json", "w") as f:
        json.dump(trajectories, f)


if __name__ == "__main__":
    main()