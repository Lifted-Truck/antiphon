# brief-antiphon-001 — ask autonomous to list ANTIPHON as deliberately dormant

- **Queue item:** unqueued — human-directed at the ratification beat. Closes
  the ROADMAP open question about ecosystem-track registration.
- **Why:** ANTIPHON is green and will stay inactive indefinitely by design.
  To anything reading activity signals, a repo with a passing oracle and no
  commits looks abandoned rather than gated. The registry entry is what makes
  the dormancy legible without opening the repo.
- **Evidence consulted:** `autonomous/registry.json` (the `synthetic-worlds`
  group rule + `derived_status` semantics — this is what showed ANTIPHON is
  *already* in ecosystem scope, correcting an earlier claim of mine that it
  was not); `autonomous/ROADMAP.md` § Execution-project registry (HYPERSAW's
  entry as the shape and precedent, registered "at human direction during its
  ratification gate"); `doctrine/INTEGRATIONS.md` §2–§3 (mailbox exception,
  ball-state frontmatter, decisions-never-live-in-integrations);
  `integrations/dispatch/brief.md` as the format exemplar.
- **Alternatives rejected:**
  - *Edit `autonomous/ROADMAP.md` directly* — rejected: rule zero, writes stay
    home. A visiting agent doesn't run the resident harness, so its commits
    bypass that repo's immune system. The brief is the sanctioned path.
  - *Also commit the brief inside autonomous* — rejected: the mailbox exception
    permits the **write**, not the commit. Left untracked for a resident there.
  - *Request a `registry.json` change too* — rejected as unnecessary and
    actively wrong: the group rule already covers immediate children of
    `synthetic-worlds`, and harness state is derived at sweep time, never
    hand-maintained. Asking for it would have added a stale hand-maintained
    fact.
  - *Also file the Wend/Tonality briefs while filing this one* — rejected:
    they would hand a provider work that must not start until the spin-up
    conditions hold. Recorded in ROADMAP so the absence reads as intentional.
- **Verify:** `./verify fast` → exit 0, 6 tests, 5 gates green. Git hash in
  `.harness/last-verify.json`.
- **Open questions:**
  1. **Ball is with autonomous** until 2026-07-28. Nothing here is blocked;
     no degraded placeholder is needed because this is a visibility listing,
     not a capability.
  2. **Dormancy has no machine-readable representation.** The brief offers to
     implement one (a field in `project.manifest.json` that sweeps can read)
     if autonomous prefers it to registry prose. A second dormant project
     would make that gap structural rather than cosmetic.
  3. **Manifest still provisional** — unchanged by this work.
