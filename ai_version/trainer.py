from game import Game
from agent import DQNAgent

def main():
    game = Game()
    agent = DQNAgent(state_size=7, action_size=5, train=True)

    no_games = 100

    for _ in range(no_games):
        state = game.reset()
        done = False

        while not done:
            action = agent.get_action(state)
            next_state, reward, done = game.step(action)
            agent.replay_buffer.push(state, action, reward, next_state, done)
            state = next_state


if __name__ == "__main__":
    main()