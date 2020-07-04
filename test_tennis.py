import unittest

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))


from tennis import Match, Game


class MatchTestCase(unittest.TestCase):

    def test_score_with_no_points(self):
        match = Match()
        self.assertEqual(match.score(), "0-0")


class GameTestCase(unittest.TestCase):

    def test_score_with_no_points_is_empty(self):
        game = Game()
        self.assertEqual(game.score(), "0-0")

    def test_score_with_one_point(self):
        game = Game()
        game.point_won_by("player-1")

        self.assertEqual(game.score(), "15-0")

    def test_score_with_two_points(self):
        game = Game()
        game.point_won_by("player-1")
        game.point_won_by("player-1")

        self.assertEqual(game.score(), "30-0")

    def test_score_with_three_points(self):
        game = Game()
        game.point_won_by("player-1")
        game.point_won_by("player-1")
        game.point_won_by("player-1")

        self.assertEqual(game.score(), "40-0")

    def test_score_with_mixed_points(self):
        game = Game()
        game.point_won_by("player-1")
        game.point_won_by("player-2")
        game.point_won_by("player-1")

        self.assertEqual(game.score(), "30-15")


if __name__ == '__main__':
    unittest.main()
