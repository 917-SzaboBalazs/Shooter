import unittest
from game import Game, PLAYER_SPEED, PLAYER_START_X, PLAYER_START_Y

# Write unit test class
class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def test_move_left(self):
        self.game.reset()
        new_state = self.game.step((1, 0, 0, 0, 0))
        
        self.assertEqual(new_state[0][0], PLAYER_START_X - PLAYER_SPEED)
        self.assertEqual(new_state[0][1], PLAYER_START_Y)
        self.assertEqual(new_state[1], 0)
        self.assertEqual(new_state[2], False)

    def test_move_right(self):
        self.game.reset()
        new_state = self.game.step((0, 1, 0, 0, 0))
        
        self.assertEqual(new_state[0][0], PLAYER_START_X + PLAYER_SPEED)
        self.assertEqual(new_state[0][1], PLAYER_START_Y)
        self.assertEqual(new_state[1], 0)
        self.assertEqual(new_state[2], False)

    def test_move_up(self):
        self.game.reset()
        new_state = self.game.step((0, 0, 1, 0, 0))
        
        self.assertEqual(new_state[0][0], PLAYER_START_X)
        self.assertEqual(new_state[0][1], PLAYER_START_Y - PLAYER_SPEED)
        self.assertEqual(new_state[1], 0)
        self.assertEqual(new_state[2], False)

    def test_move_down(self):
        self.game.reset()
        new_state = self.game.step((0, 0, 0, 1, 0))
        
        self.assertEqual(new_state[0], [])
        self.assertEqual(new_state[1], -1)
        self.assertEqual(new_state[2], True)

    def test_shoot(self):
        self.game.reset()
        new_state = self.game.step((0, 0, 0, 0, 1))
        
        self.assertEqual(new_state[0][0], PLAYER_START_X)
        self.assertEqual(new_state[0][1], PLAYER_START_Y)
        self.assertEqual(new_state[1], 0)
        self.assertEqual(new_state[2], False)
