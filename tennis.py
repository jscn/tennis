#!/usr/bin/env python3
"""
Tennis scoring.
"""


class Game:
    """A single Game in a Set."""

    MINIMUM_POINTS = 4
    MINIMUM_LEAD = 2

    def __init__(self, player_one, player_two):
        self.player_one = player_one
        self.player_two = player_two
        self._points = {
            self.player_one: 0,
            self.player_two: 0,
        }
        self._scores = {
            0: 0,
            1: 15,
            2: 30,
            3: 40,
        }

    def _score(self, player):
        """Return the score for the given player."""
        return str(self._scores[self._points[player]])

    def point_won_by(self, player):
        self._points[player] += 1

    def score(self):
        """Return the current score."""
        if self.winner():
            return ""

        if self._points[self.player_one] >= 3 and self._points[self.player_two] >=3:
            if self._points[self.player_one] > self._points[self.player_two]:
                return f"Advantage {self.player_one}"
            elif self._points[self.player_one] < self._points[self.player_two]:
                return f"Advantage {self.player_two}"
            else:
                return "Deuce"

        return "-".join([
            self._score(self.player_one),
            self._score(self.player_two),
        ])

    def winner(self):
        """Return the winner of the game."""
        if (self._points[self.player_one] >= self.MINIMUM_POINTS and
            self._points[self.player_one] - self._points[self.player_two] >= self.MINIMUM_LEAD):
            return self.player_one
        if (self._points[self.player_two] >= self.MINIMUM_POINTS and
            self._points[self.player_two] - self._points[self.player_one] >= self.MINIMUM_LEAD):
            return self.player_two


class TieBreakGame(Game):

    MINIMUM_POINTS = 7

    def _score(self, player):
        """Return the score for the given player."""
        return str(self._points[player])


class Set:
    """A single Set."""

    def __init__(self, player_one, player_two):
        self.player_one = player_one
        self.player_two = player_two
        self._games = [Game(self.player_one, self.player_two)]

    def point_won_by(self, player):
        if self._games[-1].winner():
            if self.games_won()[self.player_one] == 6 and self.games_won()[self.player_two] == 6:
                game = TieBreakGame(self.player_one, self.player_two)
            else:
                game = Game(self.player_one, self.player_two)
            self._games.append(game)
        self._games[-1].point_won_by(player)

    def games_won(self):
        winners = [game.winner() for game in self._games]
        return {
            self.player_one: winners.count(self.player_one),
            self.player_two: winners.count(self.player_two),
        }

    def score(self):
        """Return the current score."""
        return "-".join([
            str(self.games_won()[self.player_one]),
            str(self.games_won()[self.player_two])
        ])

    def winner(self):
        """Return the winner of the set."""
        if isinstance(self._games[-1], TieBreakGame):
            return self._games[-1].winner()

        games_player_one = self.games_won()[self.player_one]
        games_player_two = self.games_won()[self.player_two]
        if games_player_one > 6 and games_player_one > games_player_two + 2:
            return self.player_one
        if games_player_two > 6 and games_player_two > games_player_one + 2:
            return self.player_two


class Match:
    """A Tennis Match."""

    def __init__(self, player_one, player_two):
        self._set = Set(player_one, player_two)

    def point_won_by(self, player):
        self._set.point_won_by(player)

    def score(self):
        """Return the current set score followed by the current game score."""
        game_score = self._set._games[-1].score()
        set_score = self._set.score()

        if set_score and game_score:
            return ", ".join([set_score, game_score])
        return set_score
        self._set = Set(player_one, player_two)
