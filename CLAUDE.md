# Agent Charter — ANTIPHON

Everything above §Domain is the invariant harness layer. Do not edit it
per-project. Project-specific facts live in §Domain and in ROADMAP.md.

## Truth contract

- **ROADMAP.md is the single source of truth.** Task state, acceptance
  criteria, invariants, and open questions live there and only there. If the
  conversation and ROADMAP.md disagree, ROADMAP.md wins; if ROADMAP.md is
  wrong, fixing it is the first task.
- **Passing ≠ done.** Done = `./verify full` green AND the ROADMAP acceptance
  criteria satisfied AND a trace entry written in `traces/`. Never collapse
  these into each other.
- **Grounded refusal is a success class.** "I cannot do this within the brief
  because X" with evidence is a correct output. Guessing to appear productive
  is a failure.
- **Reduce, never invent.** Prefer deleting code, tightening a contract, or
  reusing an existing mechanism over adding a new one. Every new abstraction
  must displace at least as much complexity as it introduces.
- **Review beats are visual-first.** When presenting completed work at a
  gate (phase close, ratification request, PR), lead with a visual — a
  self-contained HTML report, render set, or live demo — sufficient to
  evaluate the change WITHOUT reading the diff, plus evidence it works and
  open questions. Code diving is the fallback, never the ask.

## Provenance

- Every nontrivial claim about the codebase must cite its evidence: a file
  path and line, a verify run, or a ROADMAP entry. No provenance → phrase it
  as a hypothesis, not a fact.
- Every merged change gets an entry in `traces/` (see the provenance skill):
  what changed, why, evidence consulted, verify result + git hash.

## Delegation policy (lead session)

- The lead plans, delegates, integrates, and is the **only** writer of
  ROADMAP.md. Subagents never touch it.
- Delegation briefs are self-contained: subagents start with zero conversation
  history. Every brief states (1) files in scope, (2) acceptance criteria
  copied verbatim from ROADMAP.md, (3) the verify target, (4) what is
  explicitly out of scope.
- Use built-in Explore for codebase reconnaissance. Use `implementer` for
  scoped changes, `verifier` for oracle runs, `critic` (Opus) for adversarial
  review of anything architectural, irreversible, or touching an invariant.
- One queue item per implementer dispatch. Parallel dispatches only for items
  with disjoint file scopes.
- Do not start work on an item whose acceptance criteria are missing or
  ambiguous. Surface the gap to the human; that is the deliverable.

## Oracle discipline

- Run `./verify fast` after any change set; `./verify full` before declaring
  a queue item done. Report oracle output verbatim — never summarize a failure
  into vagueness.
- A red oracle halts forward work. Fix or revert; do not stack changes on red.
- Never weaken a gate (skip a test, relax a threshold, mark xfail) without an
  explicit human decision recorded in ROADMAP.md.

## Human gates

Stop and ask before: deleting files, changing the public interface of
anything, editing `./verify` or the gates it runs, adding a dependency,
any git operation beyond add/commit on the working branch, and anything §Domain
lists as protected.

---

## §Domain — ANTIPHON

**What this is.** A quantized harmonic companion for Ableton Live. It hears a
live MIDI performance on a source track, derives a **causal** harmonic spine
under θ/k hysteresis, and emits complementary MIDI into its own target track
on the transport grid (bar-quantized by default). It is explicitly *not* a
real-time harmonizer, and it is *not* an offline harmonizer — that is Wend's
`harmonize` mode. ANTIPHON owns the **live regime** only.

**Status: scaffolding only.** Three spin-up conditions in
`project.manifest.json` remain UNMET (Wend H2 not passed; no demonstrated
live-regime need; quantization ceiling not measured). Feature work is gated on
them. What exists today is the harness plus the surviving hysteresis kernel.

**Stack & entrypoints.** Python ≥3.11, **zero runtime dependencies**, no
framework. Core: `src/antiphon/core/` (pure). Adapters: `src/antiphon/adapters/`
(the only place I/O, wall-clock, or Tonality may appear). Tests: stdlib
`unittest`, `PYTHONPATH=src python3 -m unittest discover -s tests -t .`.
No `main()` yet — there is no runnable device until Phase 1.

**Domain invariants** (the critic checks against these; all five are gated in
`./verify`):
1. **No wall-clock in the core.** Scheduling is in transport time (beats).
   The runner may touch time; `core/`, `policies/`, `emit/` may not. (D1, D5)
2. **No unseeded randomness.** Policies receive a seeded `random.Random`
   instance; bare `random.*` module calls are forbidden. (D5)
3. **No AI/LLM in the runtime path.** Agents build and review; they never
   perform. (D5)
4. **Tonality only inside its adapter.** New oracle surface = provider-first
   PR to Tonality + linked pin bump here. Never shim locally. (D2)
5. **Consume, don't fork.** ANTIPHON produces spines conforming to Wend's
   frozen `HarmonicSpine` (`source: "live"`) and pins Wend's voice stage for
   realization. It does not define rival contracts. (D7)

**Protected paths** (human gate to change):
- `src/antiphon/core/hysteresis.py` + `tests/test_hysteresis.py` — behavior is
  **pinned**. This kernel survived the Wend migration deliberately; changing it
  requires an appended DECISIONS entry, not a refactor.
- `verify` and the gates it runs · `DECISIONS.md` (append-only) · `.claude/`

**Verify targets.** `fast` (~1s): leak gate, no-wall-clock, no-unseeded-random,
Tonality-boundary, zero-dep, then 6 hysteresis behavior tests. `full`: runs
`fast`, then reports that **Layer-E is not yet implemented** — it is blocked on
Wend's frozen spine schema (ROADMAP Phase 1). This is deliberate: an
aspirational red gate trains the reflex of ignoring red.

**The replay invariant** (Layer-E, owed): every live session logs its causal
spine stream + params + seed; replaying that log through Wend's `voice` must
reproduce the session's emissions byte-for-byte. **The batch tool is the live
device's oracle.** Build this harness before any musical feature work.
