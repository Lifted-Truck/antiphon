# dormancy-ratification — integrate autonomous's answer to antiphon-001

- **Queue item:** ROADMAP Phase 0 — closes the manifest ratification gate and
  the `antiphon-001` exchange.
- **Why:** autonomous accepted the registry listing and then corrected the ask:
  `governor/monitor.py` does not read ROADMAP.md, so the prose listing the
  brief requested makes dormancy legible to humans while leaving the governor
  as blind as before. The machine-readable `dormant` block is the half that
  actually addresses the brief's own stated motivation. Integrated it, plus the
  local contract test.
- **Evidence consulted:** `autonomous/integrations/antiphon/response.md`;
  `autonomous/governor/monitor.py:99-121` (`manifest_dormant`, the
  `review_by`-required guard) and `:167-184` (expired → `DORMANT-EXPIRED` WARN
  plus restored `STALE`); `autonomous/governor/test_monitor.py::TestDormancy`
  (4 cases). The response's description was checked against the implementation
  before adopting it, not taken on trust — the two match.
- **Alternatives rejected:**
  - *Take the spec from the response alone* — rejected: writing a manifest
    field to a described contract rather than the implemented one is how a
    silently-ignored block happens. Reading `monitor.py` cost minutes.
  - *Bump the README `Last verified` date to dodge `STALE`* — rejected as
    date-gaming. Dormancy is the sanctioned mechanism; the date moved to
    2026-07-14 only because the README genuinely changed and was re-checked
    today.
  - *Skip the contract test (autonomous marked it optional)* — rejected:
    monitor's malformed-block rule (ignore, fall back to `STALE`) is correct
    for the fleet but gives this repo no signal, so a dropped `review_by` would
    be invisible from inside ANTIPHON until someone read a sweep we do not run.
  - *A non-time-dependent shape test* — rejected: it would assert the block is
    well-formed while saying nothing about whether it has lapsed, which is the
    failure mode that matters. The time dependence IS the deadline.
- **Verify:** `./verify fast` → exit 0. 10 tests (6 hysteresis + 4 dormancy),
  5 Layer-0 gates. The new gate was negative-tested per L0003: dropping
  `review_by` → red; back-dating `review_by` → red; manifest restored → green.
- **Open questions:**
  1. **2026-10-13 is now a hard date.** `test_dormancy_has_not_expired` goes
     red with no diff. Re-ratification must be an appended DECISIONS entry
     re-examining the three spin-up conditions — if it degenerates into bumping
     the date, the expiry has become the permanent mute it was designed to
     prevent (D11's falsifier).
  2. **Fixture offered to autonomous, unanswered.** The same four assertions as
     a manifest-shape fixture for their CI; would be consumer-authored,
     resident-landed. Not blocking either side.
  3. **Withdrew an unevidenced claim.** The brief asserted "a second dormant
     project would make the gap structural" without surveying for one. Their
     53 WARN / 58 repos (21 `STALE`) is the first actual evidence about the
     population and points the same way without my assumption.
  4. **Flagged for any fleet retrofit:** a bulk rollout is exactly where
     `review_by` gets filled in uniformly to clear a dashboard, and the field
     cannot distinguish a defended date from a reflexive one. The per-repo
     decision defending the date is the part worth mandating.
