"""Pin the hysteresis kernel's behavior. These run today (the kernel is real).

Ported verbatim from the starter kit's pytest suite, expressed in stdlib
unittest: the core is zero-dep by charter, and a test dependency would be the
first crack in that. The six assertions are unchanged -- this is the behavior
contract for the surviving kernel, not a rewrite of it.
"""

import unittest

from antiphon.core.hysteresis import (
    Candidate, HysteresisConfig, HysteresisState, step,
)

CFG = HysteresisConfig(theta=0.10, k=2)


def r(*pairs):
    return [Candidate(label, conf) for label, conf in pairs]


class TestHysteresis(unittest.TestCase):

    def test_adopts_first_candidate_immediately(self):
        s, switched = step(HysteresisState(), r(("C major", 0.6)), CFG)
        self.assertTrue(switched)
        self.assertEqual(s.held, "C major")

    def test_holds_against_subthreshold_challenger(self):
        s = HysteresisState(held="C major", frames_held=4)
        s, switched = step(s, r(("G major", 0.55), ("C major", 0.50)), CFG)
        self.assertFalse(switched)
        self.assertEqual(s.held, "C major")
        self.assertIsNone(s.challenger)

    def test_challenger_needs_k_consecutive_frames(self):
        s = HysteresisState(held="C major", frames_held=4)
        ranked = r(("G major", 0.70), ("C major", 0.50))
        s, sw1 = step(s, ranked, CFG)
        self.assertFalse(sw1)
        self.assertEqual(s.challenger, "G major")
        self.assertEqual(s.challenger_streak, 1)
        s, sw2 = step(s, ranked, CFG)
        self.assertTrue(sw2)
        self.assertEqual(s.held, "G major")
        self.assertEqual(s.frames_held, 1)

    def test_streak_resets_on_different_challenger(self):
        s = HysteresisState(held="C major", frames_held=4,
                            challenger="G major", challenger_streak=1)
        s, switched = step(s, r(("F major", 0.75), ("C major", 0.50)), CFG)
        self.assertFalse(switched)
        self.assertEqual(s.challenger, "F major")
        self.assertEqual(s.challenger_streak, 1)

    def test_incumbent_absent_from_ranking_counts_as_zero_confidence(self):
        s = HysteresisState(held="C major", frames_held=4)
        s, _ = step(s, r(("A minor", 0.12)), CFG)
        self.assertEqual(s.challenger, "A minor")  # 0.12 - 0.0 >= theta

    def test_empty_ranking_holds(self):
        s = HysteresisState(held="C major", frames_held=4)
        s, switched = step(s, [], CFG)
        self.assertFalse(switched)
        self.assertEqual(s.held, "C major")
        self.assertEqual(s.frames_held, 5)


if __name__ == "__main__":
    unittest.main()
