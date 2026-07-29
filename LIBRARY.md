# LIBRARY — ANTIPHON

Durable, hard-won lessons. Entry format is the leaf format used across the
tree, so a parent audit loop can harvest this file with the same procedure it
uses on any sibling. Every entry keeps its `evidence:` and `falsifier:`.

---

### L0001 — A gate that has never fired is not known to be a gate
**tag:** `oracle-boundary` · **tier:** candidate · **added:** 2026-07-13

`./verify fast` went green the first time it ran to completion. That is exactly
the situation where a *silently broken* gate is indistinguishable from a
*passing* one — a grep with a wrong pattern matches nothing and reports
success, which is how the ecosystem's own leak scanner once shipped blind
(see the `POSIX ERE — no \s` warning inside `verify`).

So: after writing a gate, deliberately violate it and confirm it goes red, and
confirm the *near-miss* case stays green. Here that meant planting a
`time.time()` in `core/`, a bare `random.choice(`, an `import tonality` outside
the adapter, and a `/Users/...` path — all four fired — plus a seeded
`rng.choice(...)` which correctly did **not** fire.

**evidence:** the five-case negative test run at scaffolding; `verify` gates
`no_wallclock_gate`, `no_unseeded_random_gate`, `tonality_boundary_gate`,
`leak_gate`, and the leading-char class `(^|[^.[:alnum:]_])` that distinguishes
`random.choice(` from `rng.choice(`.
**falsifier:** a gate that passes its negative test but still misses a real
violation in practice (e.g. a `from time import time` import form, which the
current pattern does **not** catch) — which would show the negative test was
too narrow, not that the practice is wrong.

---

### L0002 — When two project docs disagree, ruling which wins is a decision, not a merge
**tag:** `determinism-replay` · **tier:** candidate · **added:** 2026-07-13

ANTIPHON's directory held a starter kit describing an *offline* device and a
newer STATUS doc redefining it as a *live* device and marking most of the
starter "do not resurrect." Scaffolding "what was there" would have published
the superseded design to a public remote, where the next fresh-context session
would have read it as current truth — the failure is silent and compounding,
because scaffolded code reads as more authoritative than the prose that
deprecates it.

The resolution is not to reconcile the two documents by judgment mid-task. It
is to surface the contradiction to the human, get an explicit precedence
ruling, and record that ruling as an appended decision (here, D7) naming
exactly what survives and what is superseded. Composite and long-dormant
projects accrete docs at different times; precedence must be *pinned*, not
inferred.

**evidence:** `ANTIPHON_STATUS.md` (2026-07-13) vs `antiphon-starter.zip`
(same date, earlier content); DECISIONS D7; the zip is gitignored rather than
scaffolded.
**falsifier:** a case where the older document was in fact the current one and
the newer was an abandoned draft — which would show recency is the wrong
tiebreak and that the human ruling (not the timestamp) is doing the real work.

---

### L0003 — A triage that lists what it recognizes silently drops the remainder
**tag:** `oracle-boundary` · **tier:** candidate · **added:** 2026-07-13

Decision D7 triaged the starter kit into "ported" and "superseded" and read as
complete. It was not: it enumerated the files whose fate was *salient* — the
policy stubs, the schemas, the adapter — and was simply silent on five others.
Silence is not a verdict, but in a two-column table it looks exactly like one.
D7 even asserted the bridge sketch "survives" while nothing in the repo
actually captured it, so the document disagreed with the tree and neither
noticed.

The failure only surfaced because deletion forced a re-read of the *source*
rather than the summary. Generalisation: when triaging a bundle for deletion,
enumerate the artifact's own contents and mark a verdict against **every**
item, including "read, discarded" — an unmentioned file is an untriaged file.
The check is cheap and the loss is irreversible, which is a poor trade to get
wrong.

**evidence:** D7 vs D10; the five unaccounted files (`policies/base.py`
P1–P6, `tests/fixtures/README.md`, `adapters/live_bridge.py`,
`core/window.py`, `emit/clip_writer.py`), each holding live-regime design
recorded nowhere else; `docs/inherited-design.md` now holds them.
**falsifier:** a triage where per-item enumeration produces only noise — every
unmentioned item genuinely worthless — which would show the discipline costs
more attention than it saves on small or homogeneous bundles.
