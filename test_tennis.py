import unittest

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))


from tennis import Match, Game, Set, TieBreakGame


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

    def test_deuce_for_four_points(self):
        game = Game()
        for _ in range(4):
            game.point_won_by("player-1")
            game.point_won_by("player-2")

        self.assertEqual(game.score(), "Deuce")

    def test_deuce_for_five_points(self):
        game = Game()
        for _ in range(5):
            game.point_won_by("player-1")
            game.point_won_by("player-2")

        self.assertEqual(game.score(), "Deuce")

    def test_advantage_player_one_for_four_points(self):
        game = Game()
        for _ in range(4):
            game.point_won_by("player-1")
        for _ in range(3):
            game.point_won_by("player-2")

        self.assertEqual(game.score(), "Advantage player-1")

    def test_advantage_player_two_for_four_points(self):
        game = Game()
        for _ in range(3):
            game.point_won_by("player-1")
        for _ in range(4):
            game.point_won_by("player-2")

        self.assertEqual(game.score(), "Advantage player-2")

    def test_player_one_wins_all(self):
        game = Game()
        for _ in range(5):
            game.point_won_by("player-1")

        self.assertEqual(game.winner(), "player-1")

    def test_player_two_wins_all(self):
        game = Game()
        for _ in range(5):
            game.point_won_by("player-2")

        self.assertEqual(game.winner(), "player-2")

    def test_player_one_ahead_by_one_no_winner(self):
        game = Game()
        for _ in range(5):
            game.point_won_by("player-1")

        for _ in range(4):
            game.point_won_by("player-2")

        self.assertIsNone(game.winner())

    def test_player_two_ahead_by_one_no_winner(self):
        game = Game()
        for _ in range(4):
            game.point_won_by("player-1")

        for _ in range(5):
            game.point_won_by("player-2")

        self.assertIsNone(game.winner())

    def test_player_one_wins_closest_possible_match(self):
        game = Game()
        for _ in range(2):
            game.point_won_by("player-2")

        for _ in range(4):
            game.point_won_by("player-1")

        self.assertEqual(game.winner(), "player-1")

    def test_player_two_wins_closest_possible_match(self):
        game = Game()
        for _ in range(2):
            game.point_won_by("player-1")

        for _ in range(4):
            game.point_won_by("player-2")

        self.assertEqual(game.winner(), "player-2")


    def test_score_is_empty_when_game_is_won(self):
        game = Game()
        for _ in range(4):
            game.point_won_by("player-1")

        for _ in range(6):
            game.point_won_by("player-2")

        self.assertEqual(game.score(), "")


class SetTestCase(unittest.TestCase):

    GAMES_TO_WIN_SET = 8
    POINTS_TO_WIN_GAME = 4
    POINTS_TO_WIN_TIE_BREAKER = 7

    def test_initial_set_score(self):
        set_ = Set()

        self.assertEqual(set_.score(), "0-0")

    def test_score_when_no_games_won(self):
        set_ = Set()
        set_.point_won_by("player-1")

        self.assertEqual(set_.score(), "0-0")

    def test_score_when_player_one_wins_a_game(self):
        set_ = Set()
        for _ in range(self.POINTS_TO_WIN_GAME):
            set_.point_won_by("player-1")

        self.assertEqual(set_.score(), "1-0")

    def test_score_when_player_two_wins_a_game(self):
        set_ = Set()
        for _ in range(self.POINTS_TO_WIN_GAME):
            set_.point_won_by("player-2")

        self.assertEqual(set_.score(), "0-1")

    def test_no_initial_winner(self):
        set_ = Set()

        self.assertIsNone(set_.winner())

    def test_no_winner_if_no_games_won(self):
        set_ = Set()
        for _ in range(self.POINTS_TO_WIN_GAME - 1):
            set_.point_won_by("player-1")

        self.assertIsNone(set_.winner())

    def test_no_winner_if_one_game_won(self):
        set_ = Set()
        for _ in range(self.POINTS_TO_WIN_GAME):
            set_.point_won_by("player-1")

        self.assertIsNone(set_.winner())

    def test_winner_player_one(self):
        set_ = Set()
        for _games in range(self.GAMES_TO_WIN_SET):
            for _ in range(self.POINTS_TO_WIN_GAME):
                set_.point_won_by("player-1")

        self.assertEqual(set_.winner(), "player-1")

    def test_winner_player_two(self):
        set_ = Set()
        for _games in range(self.GAMES_TO_WIN_SET):
            for _ in range(self.POINTS_TO_WIN_GAME):
                set_.point_won_by("player-2")

        self.assertEqual(set_.winner(), "player-2")

    def test_tie_is_broken_by_player_one(self):
        set_ = Set()
        for _games in range(6):
            for _ in range(self.POINTS_TO_WIN_GAME):
                set_.point_won_by("player-1")

        for _games in range(6):
            for _ in range(self.POINTS_TO_WIN_GAME):
                set_.point_won_by("player-2")

        # Final game is a tie-breaker
        for _ in range(self.POINTS_TO_WIN_TIE_BREAKER):
            set_.point_won_by("player-1")

        self.assertEqual(set_.winner(), "player-1")

    def test_tie_is_broken_by_player_two(self):
        set_ = Set()
        for _games in range(6):
            for _ in range(self.POINTS_TO_WIN_GAME):
                set_.point_won_by("player-1")

        for _games in range(6):
            for _ in range(self.POINTS_TO_WIN_GAME):
                set_.point_won_by("player-2")

        # Final game is a tie-breaker
        for _ in range(self.POINTS_TO_WIN_TIE_BREAKER):
            set_.point_won_by("player-2")

        self.assertEqual(set_.winner(), "player-2")


class TieBreakGameTest(unittest.TestCase):

    MINIMUM_POINTS = 7
    MINIMUM_LEAD = 2

    def test_initial_winner(self):
        game = TieBreakGame()

        self.assertIsNone(game.winner())

    def test_winner_player_one(self):
        game = TieBreakGame()

        for _ in range(self.MINIMUM_POINTS + self.MINIMUM_LEAD):
            game.point_won_by("player-1")

        self.assertEqual(game.winner(), "player-1")

    def test_winner_player_two(self):
        game = TieBreakGame()

        for _ in range(self.MINIMUM_POINTS + self.MINIMUM_LEAD):
            game.point_won_by("player-2")

        self.assertEqual(game.winner(), "player-2")

    def test_player_one_wins_closest_possible_tiebreaker(self):
        game = TieBreakGame()
        for _ in range(5):
            game.point_won_by("player-2")

        for _ in range(7):
            game.point_won_by("player-1")

        self.assertEqual(game.winner(), "player-1")

    def test_player_two_wins_closest_possible_tiebreaker(self):
        game = TieBreakGame()
        for _ in range(5):
            game.point_won_by("player-1")

        for _ in range(7):
            game.point_won_by("player-2")

        self.assertEqual(game.winner(), "player-2")

    def test_score_with_no_points(self):
        game = TieBreakGame()

        self.assertEqual(game.score(), "0-0")

    def test_score_with_player_one_points(self):
        game = TieBreakGame()
        game.point_won_by("player-1")
        game.point_won_by("player-1")
        game.point_won_by("player-1")

        self.assertEqual(game.score(), "3-0")

    def test_score_with_player_two_points(self):
        game = TieBreakGame()
        game.point_won_by("player-2")
        game.point_won_by("player-2")

        self.assertEqual(game.score(), "0-2")

    def test_score_with_mixed_points(self):
        game = TieBreakGame()
        game.point_won_by("player-2")
        game.point_won_by("player-1")
        game.point_won_by("player-2")
        game.point_won_by("player-2")
        game.point_won_by("player-2")

        self.assertEqual(game.score(), "1-4")

    def test_score_is_empty_when_game_is_won(self):
        game = TieBreakGame()
        for _ in range(self.MINIMUM_POINTS + self.MINIMUM_LEAD):
            game.point_won_by("player-2")

        self.assertEqual(game.score(), "")

if __name__ == '__main__':
    unittest.main()
