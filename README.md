# ANTIPHON

*Call-and-response. A quantized harmonic companion for Ableton Live.*

**Status: scaffolding only — not yet a runnable device.**
*Last verified current: 2026-07-13.*

ANTIPHON hears a live MIDI performance on a source track, derives a **causal**
harmonic interpretation of it under θ/k hysteresis, and emits complementary
MIDI into its own target track — scheduled on the transport grid (bar-quantized
by default), never on the wall clock.

It is deliberately **not** two things:
- **Not a real-time harmonizer.** Analysis and emission are quantized to the
  transport grid, which is what keeps the core pure, replayable, and
  verifiable. An accompanist responds to phrases, not samples.
- **Not an offline harmonizer.** That moved to [Wend](../Wend)'s two-stage
  `harmonize` mode (hear → `spine.json` → voice). ANTIPHON owns the **live
  regime** only: causal decisions, Ableton I/O, latency budgets.

## What exists today

| Component | State |
|---|---|
| θ/k hysteresis kernel + 6 pinned tests | **real, behavior-pinned** |
| Harness: `./verify`, hooks, CI, charter, decision log | **real** |
| Spine production (bridge clip-poll listener) | not built — Phase 1 |
| Emission via Wend's pinned voice stage | not built — Phase 1 |
| M4L `midiin` tap (true live input) | not built — Phase 2 |

Everything in the "not built" rows is blocked, deliberately. See
**spin-up conditions** below.

## The one novel idea: harmonic hysteresis

A tonal analyzer returns *plural ranked* candidates, and naive per-frame
re-harmonization flickers on ambiguous passages (a ii–IV pun, a suspended
chord). ANTIPHON holds its current interpretation until a challenger exceeds
the incumbent's confidence by margin **θ** for **k consecutive frames**.

That gives the device musical *inertia*, and it makes every emission
explainable: *"held C major because the challenger's margin never cleared θ."*
Rate-independent memory applied to tonal context.

The kernel is [`src/antiphon/core/hysteresis.py`](src/antiphon/core/hysteresis.py) —
pure, deterministic, state-in/state-out. Its behavior is pinned by
[`tests/test_hysteresis.py`](tests/test_hysteresis.py) and is a protected path.

## Signal flow (target architecture, Phase 1+)

```
┌──────────────────────── Ableton Live ────────────────────────┐
│  [Source track: performance]        [Target track: ANTIPHON] │
└────────┬─────────────────────────────────────▲───────────────┘
         │ note events / clip poll             │ clip write @ bar
         ▼ (AbleMCP bridge; M4L tap in Ph.2)   │ (bridge)
   ┌───────────┐                        ┌──────┴──────┐
   │ LISTENER  │                        │   EMITTER   │
   │  rolling  │                        │  Wend voice │
   │  window   │                        │  (pinned)   │
   └─────┬─────┘                        └──────▲──────┘
         │ WindowedPerformance                 │ realized notes
         ▼                                     │
   ┌───────────┐    ranked, evidenced   ┌──────┴──────┐
   │  ORACLE   │ ─────────────────────▶ │ HYSTERESIS  │
   │ (Tonality │      candidates        │  hold until │
   │  adapter) │                        │  θ for k    │
   └───────────┘                        └──────┬──────┘
                                               │ HarmonicSpine (source:"live")
                                               ▼  [Wend's frozen schema]
```

## Spin-up conditions (all three must hold before feature work)

Recorded in `ANTIPHON_STATUS.md` and tracked in `project.manifest.json`:

1. **Wend H2 passes** — the falsifiable musical claim (harmonization clarifies
   hearing) holds on the fixture set. No point building a live device around an
   idea that hasn't earned it in batch. — **unmet**
2. **Demonstrated need for the live regime** — an actual workflow blocked by
   batch (performing against it, not bouncing files). — **unmet**
3. **Quantization ceiling chosen from measurement** — bar-level works on the
   Python daemon + AbleMCP bridge today; beat/sub-beat waits on tonality-core
   slice availability. — **unmet**

This ordering is the rung doctrine applied honestly: standing up a new repo
before the current home is the demonstrated bottleneck is escalation by
default. The repo exists so the decisions are recorded and the surviving kernel
has a home — not because the work is ready to start.

## Verify

```bash
./verify fast
```

Layer-0, deterministic, CI-blocking, ~1s: leak gate · no wall-clock in core ·
no unseeded randomness · Tonality-import boundary · zero-dep charter · 6
hysteresis behavior tests.

`./verify full` runs `fast` and then honestly reports that **Layer-E is not
implemented yet** — it is blocked on Wend's frozen spine schema. The owed
Layer-E is the **replay invariant**: replaying a logged session's causal spine
+ params + seed through Wend's `voice` must reproduce that session's emissions
byte-for-byte. *The batch tool is the live device's oracle.*

## Relationship to the rest of the ecosystem

- **Wend** — provider. ANTIPHON consumes the frozen `HarmonicSpine` schema and
  pins the voice stage. Consume, don't fork.
- **Tonality** — provider. Pinned library import behind an adapter; the MCP
  server is the dev surface only, never the runtime path. New oracle surface is
  a provider-first PR there, then a linked pin bump here.
- **AbleMCP bridge** — clip read/write and transport state for Phase 1.

## Map

| File | What it holds |
|---|---|
| `ROADMAP.md` | Single source of direction; phase gates |
| `DECISIONS.md` | Append-only record (D1–D7) |
| `CLAUDE.md` | Agent charter; §Domain holds the invariants |
| `ANTIPHON_STATUS.md` | Why this is on ice; what survived the Wend migration |
| `project.manifest.json` | Spin-up survey answers (provisional until ratified) |
| `INDEX.md` / `LIBRARY.md` | Knowledge loop: durable lessons |
| `traces/` | One entry per merged change |
