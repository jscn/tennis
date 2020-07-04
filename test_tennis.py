import unittest

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))


from tennis import Match


class MatchTestCase(unittest.TestCase):

    def test_score_with_no_points(self):
        match = Match()
        self.assertEqual(match.score(), "0-0")


if __name__ == '__main__':
    unittest.main()
