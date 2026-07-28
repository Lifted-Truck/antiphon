# traces/

One entry per merged change set: `YYYY-MM-DD-<slug>.md`. Append-only — never
edit or delete a prior trace; correct the record with a new entry citing the
old. Format is defined by the provenance skill
(`.claude/skills/provenance/SKILL.md`):

```markdown
# <slug> — <one-line what>

- **Queue item:** <ROADMAP id or "unqueued: reason">
- **Why:** <the decision, not a diff narration>
- **Evidence consulted:** <files read, ROADMAP sections, prior traces>
- **Alternatives rejected:** <briefly, with the reason — or "none considered">
- **Verify:** <target, exit code, git hash from .harness/last-verify.json>
- **Open questions:** <anything unverified or deferred; "none" is a claim>
```

`traces/` is what makes "passing ≠ done" checkable: green oracle + satisfied
acceptance criteria + a written trace.
