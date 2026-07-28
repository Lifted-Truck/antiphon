# DECISIONS (append-only)

Never edit or delete a prior entry. Correct the record by appending a new one
that cites the old.

## D1 — Quantized call-and-response, not real-time
**Decision:** All analysis/emission scheduled on the transport grid; default
commit at bar boundaries with ≥1 beat lookahead.
**Rationale:** Python + bridge round-trip + oracle analysis cannot meet
audio-thread latency; transport-time scheduling keeps the core pure and
replayable per the deterministic-core doctrine. Musically defensible: an
accompanist responds to phrases, not samples.
**Falsifier:** If Phase 2 latency measurements show reliable sub-beat
round-trips, beat-level or sub-beat emission may be promoted; the decision
constrains the *default*, not the ceiling. Amended by D7: the latency ceiling
moves when tonality-core's analysis slices land; the scheduling doctrine
(deterministic, transport-time, no wall-clock) does not.

## D2 — Tonality consumed as pinned library, not MCP, in the runtime path
**Decision:** The Tonality adapter imports Tonality directly; the MCP server
remains the agent/dev surface only.
**Rationale:** No serialization tax per frame; the adapter isolates ANTIPHON
from upstream API churn. Cross-repo policy applies: new oracle needs → provider
PR lands in Tonality first, ANTIPHON bumps its pin in a linked PR. Writes stay
home.
**Enforced by:** `tonality_boundary_gate` in `./verify` (negative-tested).

## D3 — Live integration via existing AbleMCP bridge first
**Decision:** Clip polling + `live_set_clip_notes` for input/output until
Phase 2, which adds a dedicated M4L `midiin` tap for live performance.
**Rationale:** Reuse proven plumbing; prove the contracts before building new
Max devices. The known limitation (recorded/playing clips only) is accepted and
phase-gated, not papered over.
**Falsifier:** assumption A1 — that clip polling has the fidelity/rate for a
1-bar-lookahead loop — is **unverified**. If it fails, Phase 2 moves up.

## D4 — Harmonic hysteresis on interpretation switching
**Decision:** The device holds its current key/chord interpretation until a
challenger exceeds the incumbent's confidence by margin θ for k consecutive
frames (θ, k configurable).
**Rationale:** An oracle returns plural ranked candidates; naive per-frame
re-harmonization flickers on ambiguous passages. Rate-independent memory gives
musical inertia and makes emissions explainable ("held because the challenger's
margin never cleared θ").
**Status:** implemented and behavior-pinned — `src/antiphon/core/hysteresis.py`,
6 tests. Protected path.
**Open (A3):** θ=0.10, k=2 are **placeholders**, never validated against real
material. Tuning is a Phase 1 item and must be traced.

## D5 — AI/deterministic boundary
**Decision:** No AI anywhere in the runtime path. Policies are deterministic
with seeded RNG; no wall-clock in core. Claude agents build and review; they do
not perform.
**Enforced by:** `no_wallclock_gate` and `no_unseeded_random_gate` in
`./verify` (both negative-tested).

## D6 — Provenance per emitted note
**Decision:** Every emitted note references the analysis frame and candidate
index that justified it.
**Rationale:** Verifiability (pitch-legality checks are exact, not statistical)
and debuggability (the Phase 3 inspector). A complement is an argued claim, not
an assertion.
**Amended by D7:** the *carrier* of that provenance is Wend's frozen
`HarmonicSpine` + voice-stage trace, not ANTIPHON's own `AnalysisFrame` /
`ComplementPlan` contracts.

---

## D7 — At spin-up, `ANTIPHON_STATUS.md` outranks `antiphon-starter.zip`
**Date:** 2026-07-13 · **Decided by:** human ruling at the spin-up survey.

**Decision:** Where the starter kit and `ANTIPHON_STATUS.md` (2026-07-13)
disagree, the STATUS document wins. Concretely, at scaffolding time:

*Ported (survives):*
- `core/hysteresis.py` + its 6 tests — the causal spine deriver for live mode.
  Ported **verbatim**; behavior pinned; now a protected path.
- Decisions D1–D6 above, with falsifiers made concrete.
- The AbleMCP bridge integration sketch (clip poll/write first, M4L tap later).

*Superseded — do NOT resurrect from the zip:*
- `tonality_adapter.py` stub → Wend's `oracle.py` seam.
- SUSTAIN / COUNTER / PEDAL policy stubs → Wend's `surface.py` + `parts.py`.
- `AnalysisFrame` / `ComplementPlan` contracts → Wend's frozen `HarmonicSpine`
  + voice-stage trace. **ANTIPHON consumes the frozen spine schema; it does not
  define its own.**
- The starter ROADMAP's offline phases (fixture clip → complement clip).

**Rationale:** The offline harmonizer moved into Wend as the two-stage
`harmonize` mode. ANTIPHON is now the *live* companion, spun up only when its
runtime regime is genuinely in play. Scaffolding the zip as-is would have
re-created, on a public remote, exactly the design the STATUS doc marks "do not
resurrect" — and a future fresh-context session would have read it as current.

**Consequence:** `antiphon-starter.zip` is **gitignored** — kept on disk for
archaeology, untracked so it cannot be mistaken for current truth. Deleting it
outright is a human gate (see ROADMAP open questions).

**Falsifier:** If Wend's `harmonize` mode is abandoned or its spine schema
never freezes, the consume-don't-fork obligation has no provider and this
decision must be revisited — ANTIPHON would then need its own contracts, which
is a DECISIONS-level change, not an implementation detail.

## D8 — Architecture rung: single-threaded agent
**Date:** 2026-07-13 · **Decided by:** human, from the three-rung menu.

**Decision:** One resident agent; read-only subagents (`Explore`, `verifier`,
`critic`) dispatched ad hoc. Not rung 2 (thread + standing verifier), not
rung 3 (organ fleet).
**Rationale:** Doctrine requires the rung be *asked, never defaulted*, and each
rung *earned* by demonstrated bottleneck. ANTIPHON is one small deterministic
core with one seam; there is no parallelizable verifiable work to justify the
~15× token multiplier.
**Escalation trigger (pre-registered):** if live-regime verification (Layer-E
latency + replay runs) becomes the pacing item, that earns rung 2 — a standing
verifier — and nothing more. Record the bottleneck evidence here before
escalating.

## D9 — The core is zero-dependency; tests are stdlib `unittest`
**Date:** 2026-07-13 · **Decided by:** agent at scaffolding, ratifiable.

**Decision:** No runtime or test dependencies. The starter kit's pytest suite
was ported to stdlib `unittest` with all six assertions unchanged.
**Rationale:** Doctrine calls for pure, framework-free cores. `pytest` was not
installed in this environment, and adding a dependency to run six assertions
that stdlib runs identically fails the reduce-never-invent test. Zero-dep also
lets CI skip an install step entirely.
**Enforced by:** `zero_dep_gate` in `./verify` (fails on a non-empty
`requirements.txt`).
**Falsifier:** If Phase 1's replay harness genuinely needs a library that
stdlib cannot cover (e.g. a MIDI or schema-validation package), that is a human
gate and an appended decision — not a quiet `pip install`.
