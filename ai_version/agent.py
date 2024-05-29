import random

from torch import optim, nn
import torch

from utils import one_hot_encode
from model import ReplayBuffer, DQN


class DQNAgent:
    def __init__(self, state_size, action_size, hidden_dim=64, lr=0.01, gamma=0.99, buffer_capacity=10000, batch_size=64,
                 epsilon_start=0.8, epsilon_end=0.01, epsilon_decay=5000, train=False):
        self.state_size = state_size
        self.action_size = action_size
        self.gamma = gamma
        self.batch_size = batch_size

        self.model = DQN(state_size, action_size, hidden_dim)
        self.target_model = DQN(state_size, action_size, hidden_dim)
        self.target_model.load_state_dict(self.model.state_dict())
        self.target_model.eval()

        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        self.loss_fn = nn.MSELoss()

        self.replay_buffer = ReplayBuffer(buffer_capacity)
        self.epsilon = epsilon_start
        self.epsilon_end = epsilon_end
        self.epsilon_decay = epsilon_decay
        self.steps_done = 0
        self.perform_training = train

    def get_action(self, state):
        self.steps_done += 1
        if random.random() > self.epsilon:
            with torch.no_grad():
                state = torch.FloatTensor(state).unsqueeze(0)
                q_values = self.model(state)
                action = q_values.max(1)[1].item()
        else:
            action = random.randrange(self.action_size)

        self.epsilon = max(self.epsilon_end, self.epsilon - (1 / self.epsilon_decay))

        if self.perform_training:
            self.train()

        if self.perform_training and self.steps_done % 1 == 0:
            self.update_target_model()
            
        return action

    def forward(self, state):
        with torch.no_grad():
            q_values = self.model(state)
        return q_values

    def train(self):
        if len(self.replay_buffer) < self.batch_size:
            return None

        state, action, reward, next_state, done = self.replay_buffer.sample(self.batch_size)

        state = torch.FloatTensor(state)
        next_state = torch.FloatTensor(next_state)
        action = torch.LongTensor(action)
        reward = torch.FloatTensor(reward)
        done = torch.FloatTensor(done)

        q_values = self.model(state)
        next_q_values = self.target_model(next_state)

        q_value = q_values.gather(1, action.unsqueeze(1)).squeeze(1)
        next_q_value = next_q_values.max(1)[0]
        expected_q_value = reward + (1 - done) * self.gamma * next_q_value

        loss = self.loss_fn(q_value, expected_q_value.detach())

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return loss.item()

    def update_target_model(self):
        self.target_model.load_state_dict(self.model.state_dict())



import numpy as np
import random

class QLearningAgent:
    def __init__(self, state_size, action_size, learning_rate=0.1, discount_factor=0.99, epsilon=1.0, epsilon_decay=0.8, epsilon_min=0.01):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.q_table = np.zeros((state_size, action_size))

    def get_action(self, state):
        if np.random.rand() < self.epsilon:
            return random.choice(range(self.action_size))
        else:
            return np.argmax(self.q_table[state])

    def update_q_table(self, state, action, reward, next_state):
        best_next_action = np.argmax(self.q_table[next_state])
        td_target = reward + self.discount_factor * self.q_table[next_state][best_next_action]
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.learning_rate * td_error
        
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

# Example usage:
# state_size = 10  # example state size
# action_size = 4  # example action size
# agent = QLearningAgent(state_size, action_size)

# # Simulate an episode (example values)
# state = 0
# for _ in range(100):
#     action = agent.get_action(state)
#     next_state = (state + action) % state_size
#     reward = 1  # example reward
#     agent.update_q_table(state, action, reward, next_state)
#     state = next_state
