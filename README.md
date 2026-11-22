# software-estate-is-censused

The incremental form of the estate-wide provable-result accounting,
its proof, and the evidence it was adopted on. Home of the Mirror
item from the net-new frontier register of 2026-11-21.

## What stands here

- Mirror.lean — three theorems: one append step preserves the
  accounting exactly (sound); every append sequence does (steps); a
  repo no step touches keeps its pin and its count (kept). The
  counting function is opaque, so the equality holds for every
  declaration basis. Axiom audit: propext and Quot.sound at most.
- count.py — the counting function, basis stated in its header:
  theorem declaration lines outside comments at a named pin, fetched
  through the gh route.
- mirror.py — the two accountings. The from-scratch census applies
  the counting function to every repo at a run's pins; the
  incremental accounting re-derives a count only when the repo's pin
  moved, entered, or left, and carries every other entry untouched.
- pins.json — the census pin snapshots at the closing commits of
  closed-loop runs 80 (the seed) through 84, taken from the synthesis
  repo's own pins file.
- evidence.json — both tables at every run, the recount set per run,
  and the disagreement lists (empty throughout).
- gate.py — the standing checks over the landed evidence; run by
  check.sh after the Lean build. It fails closed on the first
  disagreement.
- SPEC.md — the claim, its premises, the registered decision rule,
  and the experiment's result.

## Verified

- The Lean gate is cold green with warnings as errors at the landing
  pin; the axiom audit prints propext and Quot.sound for sound and
  steps, propext alone for kept, and nothing else.
- The incremental accounting agreed with the from-scratch census on
  every repo in closed-loop runs 81, 82, and 83, the registered
  three, and in run 84 as a confirmatory step. Exactly one pin moved
  in the window (the emergence repo, run 81); exactly that repo was
  recounted, 63 to 68 as recorded; the other 35 entries were carried.
- The counting basis matches recorded counts at exact pins on seven
  repos (listed in SPEC.md).

## Not claimed

- The one uncountable entry: the incrementally-safe content-branch
  repo does not resolve on GitHub at its census pin. Both accountings
  carry it uncounted; it is a named exclusion, not an agreement on a
  number, and it is a defect of the estate's records in its own
  right — a from-scratch re-census cannot redo it either.
- The closed-loop watch has not switched yet. The switch is the
  development route's remainder and belongs to that program's own
  landing stream.
- Counts at pins outside the window, and counts under any other
  basis, are not stated here. Where the standing annexes count
  declarations of every kind rather than theorem declarations, the
  numbers differ by that basis, not by any disagreement in this
  experiment.
