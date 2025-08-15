import gym
import torch
from dqn import DQN


def main():
    device = torch.device(
        "cuda" if torch.cuda.is_available() else
        "mps" if torch.backends.mps.is_available() else
        "cpu"
    )

    # Show simulation.
    env = gym.make("CartPole-v1", render_mode = "human")
    state, info = env.reset()
    # Load Policy network
    n_observations = len(state)
    n_actions = env.action_space.n
    policy_net = DQN(n_observations, n_actions).to(device)
    policy_net.load_state_dict(torch.load("dqn.pth"))
    policy_net.eval()
    state = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
    t = 0
    print("Initial State:", state)
    while True:
        with torch.no_grad():
            action = policy_net(state).max(1).indices.view(1, 1)
        observation, reward, terminated, truncated, _ = env.step(action.item())
        reward = torch.tensor([reward], device=device)
        env.render()
        done = terminated or truncated
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            t = 0
            state, info = env.reset()
            state = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
            print("Initial State:", state)
        else:
            state = torch.tensor(observation, dtype=torch.float32, device=device).unsqueeze(0)
        t += 1


if __name__ == "__main__":
    main()