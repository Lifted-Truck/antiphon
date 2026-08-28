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

## D10 — Starter-kit triage completed; `antiphon-starter.zip` deleted
**Date:** 2026-07-13 · **Decided by:** human, conditioned on triage being
complete. Cites and completes **D7**.

**Decision:** The starter kit was fully triaged and the zip deleted. Surviving
design content that existed in no other place is captured in
`docs/inherited-design.md`, with the parts that are real acceptance criteria
promoted into ROADMAP Phases 1–2.

**What D7 missed.** D7 accounted for the *superseded* stubs but was silent on
five files, all of which carried live-regime-relevant design not covered by
Wend:
- `policies/base.py` — emission invariants **P1–P6**. Only P6 (and P1
  partially) is gated today; **P2–P5 are owed.** P3 (register fence) and P4
  (density ceiling) are ANTIPHON's by nature — they exist because a live
  performer is playing simultaneously, which Wend's batch mode never faces.
- `tests/fixtures/README.md` — the three acceptance fixtures for the *surviving*
  θ/k kernel, including the exact claim "`modulation` switches after exactly k
  frames."
- `adapters/live_bridge.py` — the four-call bridge surface and the
  everything-crossing-this-boundary-is-beats rule. D7 asserted this sketch
  survived but nothing in the repo actually captured it.
- `core/window.py` — the canonical sort `(start_beat, pitch, duration,
  velocity)`, without which replay hash equality breaks silently.
- `emit/clip_writer.py` — commit discipline: the runner asks a *pure* scheduler
  when, the writer only writes, every plan appended to traces with its hash.

**Rationale:** The zip was gitignored and therefore the only copy; deleting it
before this triage would have destroyed design that no other document held. The
general lesson — a triage that enumerates only what it recognizes will silently
drop the remainder — is recorded as LIBRARY **L0003**.

**Falsifier:** If a future session finds itself re-deriving a starter-kit
decision that `docs/inherited-design.md` does not record, the triage was
incomplete after all, and the omission should be appended here rather than
quietly re-invented.

## D11 — Dormancy is declared machine-readably and **expires** on 2026-10-13
**Date:** 2026-07-14 · **Decided by:** agent, integrating autonomous's response
to exchange `antiphon-001`. Manifest ratified by the human the same day.

**Decision:** `project.manifest.json` carries a `dormant` block —
`since: 2026-07-13`, `review_by: 2026-10-13` — read by autonomous's
`governor/monitor.py`. `tests/test_manifest_dormancy.py` asserts the shape
locally and **goes red on the review date**.

**Rationale — what the brief got wrong.** `antiphon-001` argued that a green
repo with no commits is indistinguishable from an abandoned one *to a governor
reading activity signals*, and then asked for a ROADMAP prose listing. Monitor
does not read ROADMAP.md. The listing makes the dormancy legible to humans and
leaves the governor exactly as blind — autonomous's phrasing, which is
accurate: *"you asked for the half that doesn't fix it."* The machine-readable
field is the half that fixes it. Verified against the implementation before
adopting: `monitor.py:99-121, 167-184` and `governor/test_monitor.py`.

**Why it expires.** A permanent "ignore me" flag is precisely how an abandoned
repo hides from a health sweep. So: live → `DORMANT` (INFO), suppresses the
`STALE` activity warning; expired → `DORMANT-EXPIRED` (WARN) **and** `STALE`
returns — the expiry is louder than what it muted; `review_by` omitted → the
whole block is ignored, so the incomplete form fails toward noise rather than
silence. Security and harness checks (`UNGATED`, `NO-CI`, `LEAK`, `GAPS`) fire
regardless: a dormant repo can still be insecure.

**Defending 2026-10-13.** It is a *review* cadence, not a prediction of when
ANTIPHON wakes — which is unknowable from here, since it depends on Wend H2 and
on a live-regime need that may never materialize. Three months is short enough
that a genuinely-abandoned ANTIPHON surfaces within a quarter, and long enough
not to manufacture quarterly busywork on a project that is *supposed* to be
quiet. Without the field, ANTIPHON would have tripped `STALE` on **2026-08-12**
and joined 21 genuinely-stale repos as an indistinguishable WARN.

**The local test is deliberately time-dependent.** It reads the clock and will
go red with no diff on the review date. That is the mechanism, not a defect:
it forces re-ratification here rather than delegating the deadline to a fleet
sweep this repo does not run. The no-wall-clock invariant covers `core/`,
`policies/`, and `emit/` — the replayable runtime — and does not cover tests.

**Falsifier:** If the review date arrives and re-ratification is rubber-stamped
by bumping the date without re-examining the three spin-up conditions, the
expiry has become the permanent mute it was designed to prevent, and the
mechanism is not working. Re-ratification is an appended entry here, never an
edit to silence a gate.

## D12 — `verify` sources kit-owned gates from vendored `.kit/` (kit 2.4.0)
**Date:** 2026-08-18 · **Decided by:** human (kit_sync.py retrofit); recorded
here after the fact because `verify` is a protected path and had no record of
why it stopped being self-contained.

**Decision:** `record()` and `leak_gate()` are no longer defined inline in
`./verify`. They are vendored into `.kit/kit-gates.sh`, sourced by `verify`,
and checksummed against `.kit/MANIFEST` by a new `kit_integrity` gate. A
missing `.kit/kit-gates.sh` is a hard exit, not a skip.

**This strengthens the protected path; it does not weaken it.** Recording that
explicitly, because the diff *looks* like a self-contained gate being replaced
by an external dependency — the old inline version even carried a "DO NOT
delete; keep self-contained" comment. What actually happened:

- The vendored `leak_gate` detects **two** identity shapes: the POSIX
  `/Users|home/<name>/` form this repo already caught, **and** the Windows
  drive form, which the inline version missed entirely. Per the kit's own
  notes, `leak_gate` had drifted into ten distinct implementations across the
  fleet, nine missing the Windows pattern — while every one of those repos
  declared a `kit_version`. ANTIPHON's inline copy was one of the nine. On a
  public repo that is a real exposure, not a stylistic issue.
- It adds a `.leakcheck-allow` allowlist (for docs that legitimately contain
  the patterns) and concurrency handling so a parallel fleet probe cannot make
  our verify go red on a file that no longer exists.
- `kit_integrity` is honest about its own limits: it detects **drift**, not
  tampering, since the check lives inside a file it checks. The authoritative
  comparison is external (`kit_sync.py --check`).

**Why vendored rather than sourced from the standards repo:** CI has no
checkout of that repo, and a gate that cannot run in CI is not a gate.

**Consequence — `.kit/` MUST be committed.** Vendoring only works if the files
travel with the repo. This was verified, not assumed: a simulated CI checkout
(tracked files at HEAD plus the modified `verify`, no `.kit/`) exits 1 with
`.kit/kit-gates.sh missing`. Committed together in this change.

**Do not hand-edit `.kit/`.** Local edits make `./verify` go red by design —
the point of vendoring is that the file is byte-identical everywhere, so a repo
that customises it has silently opted out of the policy it claims to carry.
Updates come from `kit_sync.py`.

**Falsifier:** If a future kit sync ever *removes* a detector this repo relied
on, `kit_integrity` will happily pass — it verifies the file matches MANIFEST,
not that MANIFEST is good. Gate coverage regressions must be caught upstream in
the standards repo, not here.
