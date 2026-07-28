# ANTIPHON — ROADMAP

Single source of direction. Phases are gated: a phase is done when
`./verify fast` is green **and** its acceptance criteria hold **and** a trace
is written to `traces/`.

> **This ROADMAP was rewritten at spin-up (2026-07-13).** The starter kit's
> roadmap described the *offline* device (fixture clip → complement clip),
> which moved to Wend's `harmonize` mode. Per D7, `ANTIPHON_STATUS.md` wins:
> ANTIPHON owns the **live regime** only. The old phases are superseded, not
> renumbered — do not resurrect them from `antiphon-starter.zip`.

## Phase 0 — Repo exists, decisions recorded, kernel has a home ✅

- [x] Spin-up survey → `project.manifest.json` (provisional until ratified)
- [x] Harness: `./verify fast|full|report`, hooks, agents, provenance skill, CI
- [x] θ/k hysteresis kernel ported verbatim; 6 behavior tests green (stdlib
      `unittest` — the core stays zero-dep)
- [x] All five Layer-0 gates **negative-tested** (each proven to fire on a
      real violation; the seeded-`rng.choice` case proven not to false-positive)
- [x] Charter, README, DECISIONS D1–D7, knowledge loop, `traces/`
- [ ] **HUMAN GATE: ratify `project.manifest.json`** — the survey answers are
      provisional until you say otherwise.

**Acceptance:** `./verify fast` green from day zero, honestly scoped; a fresh
session can orient from README + ROADMAP + DECISIONS without reading code.

## ⛔ BLOCKED — spin-up conditions for all feature work

Phases 1–3 do not start until **all three** hold (`ANTIPHON_STATUS.md`):

1. **Wend H2 passes** — harmonization-clarifies-hearing holds on the fixture
   set. — **unmet**
2. **Demonstrated need for the live regime** — a real workflow blocked by
   batch. — **unmet**
3. **Quantization ceiling chosen from measurement** — not assumed. — **unmet**

Escalating past this gate because the work sounds interesting is exactly the
failure the rung doctrine names. If a condition is met, record *how it was
measured* in DECISIONS before opening Phase 1.

## Phase 1 — Spine production + the replay harness (BLOCKED)

Stand up the **verification backbone before any musical feature work.** This
ordering is deliberate: the replay invariant is what makes every later phase
checkable.

- [ ] **BLOCKING ASK → Wend:** is the `HarmonicSpine` schema frozen, and at
      what version? ANTIPHON consumes it (`source: "live"`) and must not define
      a rival contract (D7). File an integrations brief;
      do not shim locally, and do not wait blocked — ship a visibly-degraded
      placeholder behind the same interface if it stalls.
- [ ] **BLOCKING ASK → Wend:** is the `voice` stage importable and pinnable as
      a library (or is extraction needed)? Emission realization is Wend's, not
      ANTIPHON's.
- [ ] **BLOCKING ASK → Tonality:** which analysis slices exist today (key
      estimate w/ margins, chord naming, voice-leading distance) and at what
      pin? Provider-first PR if a needed surface is missing (D2).
- [ ] **Verify A1** — that AbleMCP clip polling + transport state has the
      fidelity/rate for a 1-bar-lookahead loop. If not, Phase 2's `midiin` tap
      moves up. *Measure it; do not assume it.*
- [ ] Session log format: causal spine stream + params + seed
- [ ] **Replay invariant in `./verify full`:** replay a logged session through
      Wend's `voice`; emissions must reproduce byte-for-byte
- [ ] Scheduler: pure function of (transport position, window, config) — no
      sleeps in core; the runner owns timing
- [ ] θ/k defaults tuned against real material and **traced** (A3: θ=0.10, k=2
      are placeholders inherited from the starter kit, never validated)

**Acceptance:** a logged session replays byte-identically through Wend's voice
stage on a second machine; A1 answered with measurements in `traces/`.

## Phase 2 — Live performance input (BLOCKED)

Clip polling cannot hear an *unrecorded* live performance.

- [ ] Minimal M4L listener device (dumb tap: note events + transport stamp)
- [ ] Beat-level / half-bar emission option
- [ ] Latency budget documented and **measured** (Layer-E, non-blocking)

## Phase 3 — Surface & policy expansion (BLOCKED)

- [ ] M4L control panel: θ, k, register fence, density, seed
- [ ] Per-note provenance inspector (debug view: *why this note?*)
- [ ] **Pre-registered Layer-E question:** does the causal θ/k spine converge
      on the offline DP decode of the same material as k grows? Measure it; the
      answer calibrates default θ/k against λ. *Pre-registered so the result is
      reported whichever way it comes out.*

## Open questions (blocking — ask the human)

- **Ratify the manifest?** (Phase 0 gate above.)
- **Is `antiphon-starter.zip` safe to delete** once its surviving content is
  ported? Currently gitignored, kept on disk for archaeology. Deleting files is
  a human gate.
- **Does the working title stick?** README still records OBBLIGATO / DESCANT as
  alternates.

## Non-goals

- Sample-accurate real-time harmonization
- Offline/batch harmonization (that is Wend's `harmonize` mode)
- Audio input (MIDI only)
- Any AI/LLM call in the runtime path (D5)
- Defining harmonic contracts that rival Wend's frozen spine (D7)
