import random

from torch import optim, nn
import torch

from model import ReplayBuffer, DQN


class DQNAgent:
    def __init__(self, state_dim, action_dim, hidden_dim=64, lr=1e-3, gamma=0.99, buffer_capacity=10000, batch_size=64,
                 epsilon_start=1.0, epsilon_end=0.01, epsilon_decay=500, train=False):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.gamma = gamma
        self.batch_size = batch_size

        self.model = DQN(state_dim, action_dim, hidden_dim)
        self.target_model = DQN(state_dim, action_dim, hidden_dim)
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
            action = random.randrange(self.action_dim)

        self.epsilon = max(self.epsilon_end, self.epsilon - (1 / self.epsilon_decay))

        if self.perform_training:
            self.train()

        if self.perform_training and self.steps_done % 1000 == 0:
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
