"""Harmonic hysteresis: rate-independent memory over ranked interpretations.

The device holds its current interpretation (key or chord) until a challenger
exceeds the incumbent's confidence by margin theta for k consecutive frames.
Pure and deterministic: state in, state out. No wall-clock, no I/O.

This is the novel kernel of ANTIPHON and is implemented (not stubbed) so its
behavior is pinned by tests from day one.
"""

from dataclasses import dataclass, replace
from typing import Optional, Sequence, Tuple


@dataclass(frozen=True)
class Candidate:
    label: str          # e.g. "G major" or "Am7"
    confidence: float


@dataclass(frozen=True)
class HysteresisState:
    held: Optional[str] = None
    frames_held: int = 0
    challenger: Optional[str] = None
    challenger_streak: int = 0


@dataclass(frozen=True)
class HysteresisConfig:
    theta: float = 0.10   # required confidence margin over incumbent
    k: int = 2            # consecutive frames the challenger must clear theta


def step(
    state: HysteresisState,
    ranked: Sequence[Candidate],
    cfg: HysteresisConfig,
) -> Tuple[HysteresisState, bool]:
    """Advance one frame. Returns (new_state, switched).

    Rules:
    - Empty ranking: hold, reset challenger.
    - No incumbent yet: adopt the top candidate immediately.
    - Top candidate == incumbent: hold, reset challenger.
    - Otherwise the top candidate challenges. It must beat the incumbent's
      *current* confidence (0.0 if the incumbent fell out of the ranking)
      by >= theta, for k consecutive frames, to take over. A different
      challenger label resets the streak.
    """
    if not ranked:
        return replace(state, frames_held=state.frames_held + 1,
                       challenger=None, challenger_streak=0), False

    top = ranked[0]

    if state.held is None:
        return HysteresisState(held=top.label, frames_held=1), True

    if top.label == state.held:
        return replace(state, frames_held=state.frames_held + 1,
                       challenger=None, challenger_streak=0), False

    incumbent_conf = next(
        (c.confidence for c in ranked if c.label == state.held), 0.0
    )
    clears = (top.confidence - incumbent_conf) >= cfg.theta

    if not clears:
        return replace(state, frames_held=state.frames_held + 1,
                       challenger=None, challenger_streak=0), False

    streak = state.challenger_streak + 1 if state.challenger == top.label else 1

    if streak >= cfg.k:
        return HysteresisState(held=top.label, frames_held=1), True

    return replace(state, frames_held=state.frames_held + 1,
                   challenger=top.label, challenger_streak=streak), False
