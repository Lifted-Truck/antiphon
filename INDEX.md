# INDEX — ANTIPHON knowledge loop

Compact map of durable lessons in `LIBRARY.md`. **ORIENT** before acting: scan
this index, pull only the matching LIBRARY entries into context. **REFLECT**
before ending: if something was hard-won *and* passes the write gate, add it.

Tags (from survey Q8): `hysteresis` · `oracle-boundary` · `determinism-replay`
· `live-regime` · `bridge-fidelity`

## Write gate (strict — read before adding an entry)

An entry is admissible only if **all** hold:
1. **Evidence** — a file:line, a verify run, a measurement, or a decision. Not
   a plausible-sounding generalization.
2. **A falsifier** — what observation would make this lesson wrong. An entry
   with no falsifier is an opinion; do not write it.
3. **Durable** — a future fresh-context session on this repo benefits. Facts
   already recorded by the code, README, or DECISIONS do not belong here.

Prefer **not** writing over writing unverified: this loop feeds a parent audit
loop, so a wrong lesson propagates to siblings. If nothing qualifies, write
nothing — that is the normal outcome of most sessions.

## Entries

| ID | Tag | One line |
|---|---|---|
| L0001 | `oracle-boundary` | A gate that has never fired is not known to be a gate — negative-test each one. |
| L0002 | `determinism-replay` | When two docs disagree, ruling which one wins is a *decision*, not a merge. |
