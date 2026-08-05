"""Assert ANTIPHON's side of the dormancy contract (exchange antiphon-001).

autonomous's `governor/monitor.py` reads the `dormant` block out of
project.manifest.json. Its rule for a malformed block is deliberate: a
declaration missing `review_by` is IGNORED rather than honoured, so the
incomplete form fails toward noise instead of toward silence.

That rule is correct for the fleet and useless as feedback to us -- from this
repo, a dropped `review_by` looks like nothing at all until someone reads a
sweep we do not run. So we assert the shape here, where breaking it turns our
own oracle red.

Consumer-authored contract test, per INTEGRATIONS: this is what "we rely on X"
means, executably.
"""

import datetime
import json
import unittest
from pathlib import Path

MANIFEST = Path(__file__).resolve().parent.parent / "project.manifest.json"

REQUIRED = ("since", "reason", "review_by")
DATE_FIELDS = ("since", "review_by")


def _load():
    with MANIFEST.open() as fh:
        return json.load(fh)


class TestManifestDormancy(unittest.TestCase):

    def test_manifest_parses(self):
        """Guard the guard: every other assertion here is vacuous if the
        manifest does not parse, and monitor would equally read nothing."""
        self.assertIsInstance(_load(), dict)

    def test_dormant_block_is_complete(self):
        d = _load().get("dormant")
        self.assertIsNotNone(d, "dormant block missing; monitor would report STALE")
        for field in REQUIRED:
            self.assertIn(field, d, f"monitor ignores the whole block without {field!r}")
            self.assertIsInstance(d[field], str)
            self.assertTrue(d[field].strip(), f"{field!r} is empty")

    def test_dates_are_iso_and_ordered(self):
        d = _load()["dormant"]
        parsed = {}
        for field in DATE_FIELDS:
            try:
                parsed[field] = datetime.date.fromisoformat(d[field])
            except ValueError:  # monitor's days_since would fail the same way
                self.fail(f"{field!r} is not an ISO date: {d[field]!r}")
        self.assertLess(parsed["since"], parsed["review_by"],
                        "review_by must postdate since")

    def test_dormancy_has_not_expired(self):
        """DELIBERATELY time-dependent -- this is a deadline, not a unit test.

        Dormancy expires by design. On review_by this goes red with no diff,
        which is the entire point: it forces a human re-ratification (extend
        the date, or wake the project and drop the block) instead of letting
        the declaration quietly rot into a permanent mute. Re-ratifying is an
        appended DECISIONS entry, never a bump to shut the gate up.

        The no-wall-clock invariant covers core/, policies/, and emit/ -- the
        replayable runtime. Tests are not gated, and a deadline check is
        exactly where reading the clock is the correct behavior.
        """
        review_by = datetime.date.fromisoformat(_load()["dormant"]["review_by"])
        today = datetime.date.today()
        self.assertGreaterEqual(
            review_by, today,
            f"dormancy lapsed on {review_by} -- re-ratify with a defended new "
            f"review_by (appended DECISIONS entry), or wake the project and "
            f"remove the dormant block. Do not bump the date to silence this.",
        )


if __name__ == "__main__":
    unittest.main()
