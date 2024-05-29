from game import Game
from agent import DQNAgent, QLearningAgent
from utils import one_hot_encode
import time

def main():
    game = Game()
    agent = DQNAgent(state_size=7, action_size=5, train=True)

    no_games = 1000

    for _ in range(no_games):
        state = game.reset()
        done = False
        print(state)

        while not done:
            if len(state) == 3:
                state = state[0]
            
            action = agent.get_action(state)
            next_array = game.step(one_hot_encode(action, agent.action_size))

            next_state = next_array[0]
            reward = next_array[1]
            done = next_array[2]

            
            agent.replay_buffer.push(state, action, reward, next_state, done)

            state = next_state

        print(f"Game [{_+1}/{no_games}] - Score: {game.get_score()} - Reward: {reward} - Epsilon: {agent.epsilon}")

        # Sleep for a while
        time.sleep(2)



def train_qlearning():
    game = Game()
    agent = QLearningAgent(state_size=7, action_size=5)

    no_games = 1000

    for _ in range(no_games):
        state = game.reset()
        done = False

        while not done:
            if len(state) == 3:
                state = state[0]
            
            action = agent.get_action(state)
            next_array = game.step(one_hot_encode(action, agent.action_size))

            next_state = next_array[0]
            reward = next_array[1]
            done = next_array[2]

            agent.update_q_table(state, action, reward, next_state)

            state = next_state

        print(f"Game [{_+1}/{no_games}] - Score: {game.get_score()} - Reward: {reward} - Epsilon: {agent.epsilon}")

        # Sleep for a while
        time.sleep(2)
    



if __name__ == "__main__":
    main()
    # train_qlearning()