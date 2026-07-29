# starter-triage-completion — finish the D7 triage, then delete the zip

- **Queue item:** unqueued — closes the ROADMAP open question "is
  `antiphon-starter.zip` safe to delete?" Human approved deletion *conditioned
  on the triage being complete*; it was not, so completing it came first.
- **Why:** D7's ported/superseded table read as exhaustive but was silent on
  five of the zip's files. Since the zip was gitignored, it was the only copy —
  deleting on the strength of D7 would have destroyed live-regime design that no
  other document held. The condition the human attached to the approval was the
  thing that had not actually been satisfied.
- **Evidence consulted:** every file in `antiphon-starter.zip` read directly
  (not D7's summary of them): `policies/base.py` (P1–P6 emission invariants),
  `tests/fixtures/README.md` (the three θ/k acceptance fixtures),
  `adapters/live_bridge.py` (four-call surface + beats boundary rule),
  `core/window.py` (canonical sort for hash stability), `emit/clip_writer.py`
  (commit discipline), `tests/test_determinism.py` (genuinely superseded by the
  replay invariant). Cross-checked against DECISIONS D7 and the current tree.
- **Alternatives rejected:**
  - *Delete as approved, on D7's word* — rejected: D7 was the artifact under
    suspicion; trusting a summary to authorize destroying its source inverts
    the evidence order.
  - *Keep the zip indefinitely* — rejected: the human's actual concern was that
    nothing be lost, not that the file persist. Capturing the content satisfies
    it better than an untracked binary a future session cannot see.
  - *Put the salvage in ROADMAP* — rejected for the bulk of it: ROADMAP holds
    acceptance criteria, not design notes. Only the parts that are genuinely
    checkable criteria (P2–P5, the three fixtures, canonical ordering) were
    promoted there; the rest lives in `docs/` with a pointer, per the charter's
    "anything longer belongs in docs/" rule.
- **Verify:** `./verify fast` → exit 0, 6 tests, all five Layer-0 gates green.
  Git hash recorded in `.harness/last-verify.json`.
- **Open questions:**
  1. **P2/P5 ownership unresolved** — pitch legality and the voice-leading
     bound may belong to Wend's voice stage rather than here. Flagged in
     ROADMAP Phase 2; must be checked before implementing, since a local copy
     of a provider's invariant is exactly the fork D7 forbids.
  2. **The three fixtures do not exist** — only their specification survived.
     Authoring them is Phase 1 and is what A3 (θ/k tuning) depends on.
  3. **Manifest still provisional** — unchanged by this work.
