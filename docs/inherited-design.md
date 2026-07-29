# Inherited design notes (from the starter kit)

**What this is.** The starter kit (`antiphon-starter.zip`) was triaged and
deleted at spin-up (DECISIONS **D7**, completed in **D10**). Most of it was
superseded by Wend's `harmonize` mode. This file is where the parts that
*survived* the triage were captured, so deleting the zip lost nothing.

**Status of everything below: NOT BUILT.** These are inherited design
intentions, not implemented behavior. Nothing here is gated by `./verify`
today. Where a note becomes a real acceptance criterion, it moves into
ROADMAP.md — which outranks this file if they ever disagree.

---

## Emission invariants P1–P6

The starter's policy protocol named six rules "enforced by `./verify`, not by
trust." Only P1 (partially) and P6 are gated today; **P2–P5 are owed.**

| | Invariant | Gated today? |
|---|---|---|
| **P1** | **Determinism** — identical inputs + seed ⇒ identical plan (hash-stable) | partial: seeded-RNG gate only; no replay hash yet |
| **P2** | **Pitch legality** — every emitted note's pitch is in the pitch content of the candidate named in its provenance, unless `role == "tension"`, which requires an evidence ref | no |
| **P3** | **Register fence** — no note within `fence_semitones` of the source's `[pitch_min, pitch_max]` unless the policy declares otherwise | no |
| **P4** | **Density ceiling** — emitted onsets per beat ≤ config ceiling | no |
| **P5** | **Voice-leading bound** — VL distance from previous emission ≤ config ceiling; `None` allowed only for the first emission | no |
| **P6** | **No wall-clock, no I/O, no unseeded randomness** in policy code | **yes** — grep gates in `./verify` |

**Why P3 and P4 are ANTIPHON's and not Wend's.** They exist because a *live
performer* is playing simultaneously: the fence keeps the device out of the
performer's register, and the ceiling keeps it from crowding the texture.
Wend's batch mode has no live performer to avoid, so it has no reason to own
these. P2 and P5 may well belong to Wend's voice stage — resolve that when the
spine schema freezes, and do not implement them here before checking (D7:
consume, don't fork).

## Hysteresis acceptance fixtures

The starter specified three fixtures, and they are the acceptance tests for the
one component that survived — the θ/k kernel. They are *behavioral* tests, in
contrast to the six unit tests that pin the kernel's state transitions:

| Fixture | Material | Expected behavior |
|---|---|---|
| `unambiguous_diatonic` | clear single-key material | hysteresis should **never** switch |
| `ambiguity_pun` | a passage poised between two readings (relative major/minor, or a ii–IV pun) | **flicker suppression** — the headline claim |
| `modulation` | a real key change | **should** switch, after exactly *k* frames |

Intended to be deterministically generated and committed as **both `.mid` and
note-list JSON**, so the tests do not depend on a MIDI parser (which would also
breach the zero-dep charter, D9).

These are what θ/k should be tuned against (assumption **A3**: θ=0.10, k=2 are
unvalidated placeholders). `modulation` is the sharpest of the three — "switches
after *exactly* k frames" is an exact, falsifiable claim, not a judgment call.

## Live-bridge adapter surface

The bridge sketch D7 preserved. A deliberately dumb clip/transport surface —
Phase 2's M4L `midiin` tap lands as a *separate* module so this one stays dumb.

```
read_clip_notes(track_index, clip_index)   -> Sequence[NoteEvent]
transport()                                -> {playing, song_beat, tempo, timesig}
ensure_target_clip(track_index, clip_index, length_beats) -> None
write_clip_notes(track_index, clip_index, notes)          -> None
```

**Boundary rule (load-bearing).** Every timing value crossing this boundary is
in **beats**. The runner converts to and from anything wall-clock-ish at the
very edge; the core never sees it. This is what makes the no-wall-clock gate
enforceable rather than aspirational — the gate greps `core/`, and this rule is
why nothing in `core/` ever *needs* a clock.

The adapter performs I/O and is therefore excluded from Layer-0 by design; it
is exercised by Layer-E.

## Windowing and canonical ordering

Rolling window assembly is pure data: note events in, windowed performance out.

- `NoteEvent(pitch, start_beat, duration_beats, velocity)` — the shape that
  crosses the bridge boundary.
- Notes overlapping `[start_beat, end_beat)` are **clipped** to the window.
- **Canonical sort — `(start_beat, pitch, duration, velocity)`.** This is not
  cosmetic: downstream hashing is what makes the replay invariant checkable, and
  an unstable sort silently breaks hash equality on material that is otherwise
  identical. Any reimplementation must pin this ordering in a test.
- `source_stats` — `pitch_min` / `pitch_max` / `onset_density_per_beat` /
  `onset_beats`. These are exactly the inputs P3 and P4 need.

## Commit discipline

- Plans are written at commit-beat boundaries with **≥ 1 beat of lookahead**.
- **The runner asks a pure scheduler _when_; the writer only does the _write_.**
  Keeping the "when" pure is what keeps scheduling replayable (D1).
- Every emission is appended to `traces/` with its plan hash (JSONL,
  append-only) so emissions are auditable after the fact. This is the raw
  material the replay invariant consumes.

## Superseded — deliberately not captured

For the record, so no future session goes looking: the `AnalysisFrame` /
`ComplementPlan` JSON schemas, the SUSTAIN / COUNTER / PEDAL policy bodies, the
`tonality_adapter` stub, the pytest determinism skeleton, and the starter's
offline roadmap phases were all read and discarded under D7. They are replaced
by Wend's frozen `HarmonicSpine` + voice stage.
