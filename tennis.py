#!/usr/bin/env python3
"""
The scoring system for tennis works like this.

- A match has one set and a set has many games
- A game is won by the first player to have won at least 4 points in total and at least 2 points more than the opponent.
- The running score of each game is described in a manner peculiar to tennis: scores from zero to three points are described as 0, 15, 30, 40, respectively
- If at least 3 points have been scored by each player, and the scores are equal, the score is "deuce".

- If at least 3 points have been scored by each side and a player has one more point than his opponent, the score of the game is "advantage" for the player in the lead.

- There are many games to a set in tennis

- A player wins a set by winning at least 6 games and at least 2 games more than the opponent.

-  If one player has won six games and the opponent five, an additional game is played. If the leading player wins that game, the player wins the set 7–5. If the trailing player wins the game, a tie-break is played.
- A tie-break, played under a separate set of rules, allows one player to win one more game and thus the set, to give a final set score of 7–6. A tie-break is scored one point at a time. The tie-break game continues until one player wins seven points by a margin of two or more points. Instead of being scored from 0, 15, 30, 40 like regular games, the score for a tie breaker goes up incrementally from 0 by 1. i.e a player's score will go from 0 to 1 to 2 to 3 …etc.

- Add a score method that will return the current set score followed by the current game score

- Add a pointWonBy method that indicates who won the point

Constraints:
- Only worry about 1 set
- Don't worry about validation, assume the client passes in correct data

More information on tennis scoring can be found here https://en.wikipedia.org/wiki/Tennis_scoring_system

For example:

>>> match = Match("player 1", "player 2")
>>> match.point_won_by("player 1")
>>> match.point_won_by("player 2")
>>> match.score()
"0-0, 15-15"

>>> match.pointWonBy("player 1")
>>> match.pointWonBy("player 1")
>>> match.score()
"0-0, 40-15"

>>> match.pointWonBy("player 2")
>>> match.pointWonBy("player 2")
>>> match.score()
"0-0, Deuce"

>>> match.pointWonBy("player 1")
>>> match.score();
"0-0, Advantage player 1"

>>> match.pointWonBy("player 1")
>>> match.score();
"1-0"
"""

PLAYER_ONE = "player-1"
PLAYER_TWO = "player-2"


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
        pass

    def score(self):
        """Return the current set score followed by the current game score."""
        return "0-0"


if __name__ == '__main__':
    import doctest
    doctest.testmod()
