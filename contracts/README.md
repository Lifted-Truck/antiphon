# contracts/

**Deliberately empty.** ANTIPHON does not define its own harmonic contracts.

Per DECISIONS **D7** (consume, don't fork), the harmonic interchange format is
Wend's frozen **`HarmonicSpine`** schema. ANTIPHON produces spines with
`source: "live"` conforming to that frozen version, and pins Wend's `voice`
stage for realization.

The starter kit's `analysis_frame.schema.json` and
`complement_plan.schema.json` are **superseded** — do not resurrect them from
`antiphon-starter.zip`.

If ANTIPHON ever appears to need a contract of its own, that is a signal to
file an integrations brief against Wend (provider-first), not to write a schema
here. A local schema that shadows the provider's is the fork D7 exists to
prevent.

**What lands here later:** a *pinned copy or pointer* to the frozen Wend spine
version this repo builds against — a pin, not a definition.
