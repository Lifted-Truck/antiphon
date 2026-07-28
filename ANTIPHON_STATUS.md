# ANTIPHON — STATUS: ON ICE (deliberate deferral, not abandonment)

**Destination:** filed alongside the antiphon-starter kit (wherever it was
parked), so any future session finds the current truth next to the code
**Date:** 2026-07-13
**ball:** none — dormant until spin-up conditions met

---

## What ANTIPHON now is

The future **live** harmonic companion: a separate repo, spun up only when
its runtime regime (Ableton I/O, causal decisions, latency budgets, its own
verify surface) is actually in play. The offline harmonizer it was originally
scoped around has moved into **Wend** as the two-stage `harmonize` mode
(hear → spine.json → voice); see `WEND_BRIEF_harmonize.md`. This was the
right call under the rung doctrine: a new repo before the current home is
the demonstrated bottleneck is escalation by default.

## Spin-up conditions (all three)

1. **Wend H2 passes** — the falsifiable musical claim (harmonization
   clarifies hearing) holds on the fixture set. No point building a live
   device around an idea that hasn't earned it in batch.
2. **Demonstrated need for the live regime** — an actual workflow blocked by
   batch (performing against it, not bouncing files).
3. **Quantization ceiling chosen from measurement** — bar-level works on the
   Python daemon + AbleMCP bridge today; beat/sub-beat waits on
   tonality-core slice availability (key estimate, chord naming, VL — the
   enumerated surface in `TONALITY_BRIEF_spine-oracle-surface.md`, Ask 3).

## What survives from the starter kit (do not rebuild)

- **The θ/k hysteresis kernel + its 6 tests** (`core/hysteresis.py`,
  `tests/test_hysteresis.py`) — implemented, behavior pinned. This is the
  *causal* spine deriver for live mode: hold the incumbent interpretation
  until a challenger clears margin θ for k consecutive frames.
- **Decisions D1–D6** as drafted, with D1's falsifier now concrete: the
  latency ceiling moves when tonality-core's analysis slices land; the
  scheduling doctrine (deterministic, transport-time, no wall-clock) does not.
- The **AbleMCP bridge integration sketch** (clip poll/write for v1; M4L
  midiin tap for true live input later).

## What is superseded (do not resurrect)

- `tonality_adapter.py` stub → Wend's `oracle.py` seam (execution-verified,
  with zero-dep fallback).
- SUSTAIN/COUNTER/PEDAL policy stubs → Wend's `surface.py` + `parts.py`.
- The AnalysisFrame/ComplementPlan contracts → the HarmonicSpine artifact
  (frozen in Wend) + voice-stage trace. ANTIPHON consumes the frozen spine
  schema; it does not define its own.

## Obligations inherited at spin-up

1. **Consume, don't fork:** ANTIPHON produces spines (`source: "live"`)
   conforming to the frozen HarmonicSpine version and pins Wend's voice
   stage (or its extracted successor) for realization logic.
2. **The replay invariant is the verify backbone:** every live session logs
   its causal spine stream + params + seed; replaying that log through
   Wend's `voice` must reproduce the session's emissions byte-for-byte.
   The batch tool is the live device's oracle.
3. **Layer-E convergence question, pre-registered:** does the causal θ/k
   spine approach the offline DP decode of the same material as k grows?
   Measure it; the answer calibrates default θ/k against λ.
4. **Nothing of ANTIPHON's belongs in tonality-core:** hysteresis and decode
   are policy-side unless Tonality claims decoding upstream (Ask 1 of the
   Tonality brief) — in which case ANTIPHON delegates like everyone else.

## Spin-up brief, in one paragraph

When conditions 1–3 hold: `/spinup` a single-thread-rung repo; port the
hysteresis kernel + tests verbatim; wire spine production (bridge clip-poll
listener first, M4L midiin tap second) to the frozen spine schema; wire
emission through pinned voice; stand up the replay-invariant harness before
any musical feature work. Everything else is already decided in the
documents named above.
