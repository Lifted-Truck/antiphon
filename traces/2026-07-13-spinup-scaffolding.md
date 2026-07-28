# spinup-scaffolding — stand up the ANTIPHON repo around the surviving kernel

- **Queue item:** ROADMAP Phase 0 (all items except the manifest ratification
  gate, which is the human's).
- **Why:** ANTIPHON's directory held two mutually contradictory descriptions of
  the project. Rather than merge them by judgment, the contradiction was
  surfaced and the human ruled that `ANTIPHON_STATUS.md` outranks
  `antiphon-starter.zip` (recorded as D7), and chose the single-thread rung
  from the three-rung menu (D8). The repo was then scaffolded around what the
  STATUS doc says survives — the θ/k hysteresis kernel — rather than around the
  superseded offline design.
- **Evidence consulted:** `ANTIPHON_STATUS.md`, `HANDOFF.md`, the starter
  README/ROADMAP/DECISIONS/verify inside `antiphon-starter.zip`;
  `autonomous/ONBOARDING.md` Part 2 (8-step procedure), `autonomous/kit/README.md`
  (9-question survey), `autonomous/harness/` (charter, verify, hooks, agents,
  provenance skill), `autonomous/kit/templates/ci.github.yml`.
- **Alternatives rejected:**
  - *Scaffold the starter zip as-is* — rejected: publishes a design the STATUS
    doc marks "do not resurrect" to a public remote, where a fresh-context
    session would read it as current. (Offered to the human; not chosen.)
  - *Full live-companion build (wire Wend's spine + voice now)* — rejected:
    Wend's `HarmonicSpine` is not frozen, so the seam would be placeholder
    anyway. Deferred to Phase 1 behind explicit BLOCKING ASKs.
  - *Add pytest as a test dependency* — rejected: stdlib `unittest` runs the
    same six assertions unchanged; a dependency to avoid a rewrite that took
    minutes fails reduce-never-invent. Recorded as D9 and gated.
  - *Aspirational red Layer-E in `verify full`* — rejected: it would train the
    reflex of ignoring red. `full` reports honestly that Layer-E is unbuilt and
    names its blocker.
- **Verify:** `./verify fast` → exit 0, 6 tests, all five Layer-0 gates green.
  Each gate was additionally **negative-tested**: planted violations made
  `no_wallclock_gate`, `no_unseeded_random_gate`, `tonality_boundary_gate`, and
  `leak_gate` fire; a seeded `rng.choice(...)` correctly did not trip the
  randomness gate. One real bug was caught this way during scaffolding —
  `unittest discover -t .` failed until `tests/__init__.py` was added.
  Git hash: recorded in `.harness/last-verify.json` at the initial commit.
- **Open questions:**
  1. **Manifest not ratified** — `project.manifest.json` is `status:
     "provisional"` until the human says otherwise. This is the Phase 0 gate.
  2. **A3 unvalidated** — θ=0.10, k=2 are placeholders inherited from the
     starter kit, never tuned against real material.
  3. **A1 unverified** — AbleMCP clip-poll fidelity for a 1-bar-lookahead loop
     is assumed, not measured.
  4. **Three BLOCKING ASKs unfiled** — Wend (spine schema frozen? voice stage
     pinnable?) and Tonality (which analysis slices, at what pin?). These are
     integrations briefs, not chat requests; none filed yet because the spin-up
     conditions that would justify Phase 1 are all unmet.
  5. **No ecosystem registration requested** — ANTIPHON is not yet registered in
     autonomous's ecosystem tracks (a ROADMAP edit there is resident-only).
