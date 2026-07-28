# HANDOFF — ANTIPHON starter kit → Claude Code agent

> ## ⚠️ HISTORICAL — largely superseded (2026-07-13)
>
> This document belongs to the **offline** ANTIPHON, which moved into Wend's
> `harmonize` mode. It is kept for archaeology, not as instructions.
>
> **Current truth:** `ANTIPHON_STATUS.md` → `README.md` → `ROADMAP.md` →
> `DECISIONS.md` (**D7** rules on precedence and lists exactly what survived).
> The spin-up it asks for below has already been run.
>
> Everything under "STUBBED" is **superseded — do not implement it**. The
> assumptions A1/A2/A3 remain live and are tracked in ROADMAP Phase 1.

## What this is

Starter kit for ANTIPHON, a quantized harmonic companion for Ableton Live:
listen to a source track's MIDI, analyze via Tonality (oracle), emit
complementary MIDI to a target track via deterministic seeded policies.
Read `README.md` (concept), `ROADMAP.md` (direction — single source of
truth), `DECISIONS.md` (D1–D6, binding unless amended by appended entry).

## Spin-up

Run `/spinup` (or `/retrofit` if you init the repo first) to generate
`project.manifest.json`, the layered `CLAUDE.md` charter, and hooks per the
autonomous-paradigm standards. Survey answers implied by this kit:
single-thread agent rung (escalate only on demonstrated bottleneck),
deterministic core + thin adapters, `./verify fast|full` already sketched.

## What is real vs. stubbed

REAL (behavior pinned, do not change without a DECISIONS entry):
- `src/antiphon/core/hysteresis.py` + `tests/test_hysteresis.py` — the
  interpretation-switching kernel (theta/k margin-and-streak rule).
- `contracts/*.schema.json` v0 — freeze after Phase-0 review; additive-only after.
- `verify` Layer-0 gates: no wall-clock in core, no unseeded randomness,
  Tonality import boundary.

STUBBED (yours to implement, in ROADMAP order):
- `core/window.py` — slicing + canonical ordering + source_stats
- `adapters/tonality_adapter.py` — **first job: read the actual Tonality API
  and pin a version.** This kit deliberately does not guess Tonality's
  function names. Map: key induction w/ margins, beat-grid chord
  segmentation (ranked), voice-leading distance. If a needed surface is
  missing from Tonality, file it against Tonality (provider-first PR, linked
  consumer pin bump) — do not shim locally.
- `adapters/live_bridge.py` — wire to the AbleMCP bridge transport.
  **Verify assumption A1 before Phase 1:** that clip polling + transport
  state has enough fidelity/rate for a 1-bar-lookahead loop. If not,
  Phase 2's midiin tap moves up.
- `policies/{sustain,counter,pedal}.py`, `emit/clip_writer.py`,
  `tests/test_determinism.py`, fixtures.

## Open assumptions to verify early (traced, not assumed)

- **A1** (bridge polling fidelity — above).
- **A2** Tonality is importable as a package in this environment (memory of
  the repo says local-first Python with MCP as the exposure layer; confirm
  packaging and pin).
- **A3** Default theta=0.10, k=2 are placeholders; tune against the three
  fixtures in Phase 0 and trace the choice.

## Ways of working

Autonomous-paradigm doctrine applies in full: gates never weakened;
passing != done (green + acceptance criteria + trace); reduce-never-invent
at the oracle boundary; append-only DECISIONS; no AI in the runtime path.
