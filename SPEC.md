# Mirror — the proof estate describes itself, incrementally

## Claim

The estate-wide provable-result accounting can be maintained as an
incremental derivation over the estate's own append-only graph, so a
repo's theorem count changes only when its proof sources change, and
the full re-census the closed-loop runs now repeat becomes a check,
not the mechanism.

Registered in the net-new frontier register of 2026-11-21, item 4,
with its decision rule stated in advance: the incremental form is
adopted if it agrees with the from-scratch census on every repo in
three consecutive closed-loop runs, with any disagreement traced to
a named basis difference; a single unexplained disagreement falsifies
it. Three outcome classes were registered.

## Premises

- Theorem counting is by declaration at a named head (the standing
  census basis). The counting function used here counts declaration
  lines outside comments, with the modifiers private, protected, and
  noncomputable allowed before the keyword; it is stated in full in
  the counter's header and is shared by both accountings, so the
  comparison tests the maintenance, not the basis.
- The graph's append-only property holds as ruled: a run moves a
  repo's census pin or it does not, and nothing else about the repo
  changes between runs.

## Proof

Three theorems in Mirror.lean, over an opaque counting function, so
the equality does not depend on the basis:

- sound: one append step preserves the accounting exactly —
  recounting the stepped repo at its new pin and carrying every other
  count gives the from-scratch census of the stepped assignment.
- steps: every append sequence preserves the accounting exactly,
  by induction over the steps.
- kept: a repo no step touches keeps both its pin and its count — a
  count changes only when a step moves its own pin.

Axiom audit at the landing pin: sound and steps depend on propext
and Quot.sound; kept depends on propext alone. No other axioms, no
escape tokens, pinned Lean 4.19.0, no Mathlib.

## Experiment

The incremental accounting ran beside closed-loop runs 81, 82, and
83 (the registered three), seeded from the from-scratch census at
run 80's close, with run 84 carried as a fourth, confirmatory step
outside the registered window. The pin snapshots are the synthesis
repo's own pins file at each run's closing commit. The evidence file
holds both tables at every run.

Result: agreement on every repo in all three registered runs, and
in the confirmatory step. Across the window exactly one census pin
moved — the emergence repo at run 81 — and the incremental
accounting recounted exactly that repo, reproducing its recorded
move of 63 to 68, and carried the other 35 entries untouched. The
seed census counts 35 of 36 repos and totals 4,063 theorems under
the stated basis; the estate total after run 81 is 4,068.

One entry is a named exclusion, not an agreement: the
incrementally-safe content-branch repo does not resolve on GitHub at
its census pin, so no counting function can recount it; its pin
never moves in the window, and both accountings carry it uncounted.
The basis is calibrated at exact pins against recorded counts on
seven repos — emergence 63 and 68, redundancy-is-equivalence 217,
tensors-are-editable 14, highest-minimal-axis 58,
parametric-language-model 40, the synthesis repo 11, and
deterministic-llms 53, the last matching the executed verification
count at that same pin.

## Development route

The closed-loop watch switches to the incremental accounting; the
from-scratch census becomes its periodic control. That switch is the
closed-loop program's own landing, as with the loom's pull request
before it; this repo is the mechanism, the proof, and the evidence.
