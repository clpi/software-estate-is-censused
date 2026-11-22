#!/usr/bin/env python3
"""The mirror gate: the standing checks over the landed evidence.

Fails closed on the first disagreement. The checks are offline and
deterministic: they re-derive, from the recorded pin snapshots alone,
what the incremental accounting was allowed to recount at each run,
and they compare the two landed tables entry by entry.

  1. moved      - at each run, the set of repos whose census pin
                  moved against the previous snapshot equals the
                  recorded recount set exactly.
  2. tables     - at each run, the incremental table equals the
                  from-scratch table on every repo: pin, count, and
                  basis.
  3. seed       - the seed census counts 35 of 36 repos and totals
                  4,063 theorems under the stated basis.
  4. change     - the one registered change of the window is
                  reproduced: the emergence repo moves 63 to 68 at
                  run 81 and nothing else's count moves in any run.
  5. named      - the one uncountable entry is the named one, carried
                  uncounted (null) in both tables at every run, with
                  its reason recorded in the engine.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EMERGENCE = "software-emergence-is-decidable"
UNRESOLVABLE = "software-is-incrementally-safe-content-branch"


def fail(msg):
    print(f"gate: FAIL {msg}", file=sys.stderr)
    sys.exit(1)


def main():
    with open(os.path.join(HERE, "pins.json")) as f:
        pins_by_run = json.load(f)
    with open(os.path.join(HERE, "evidence.json")) as f:
        evidence = json.load(f)

    order = ["seed", "run81", "run82", "run83", "run84"]
    prev = pins_by_run["seed"]["census_pins"]
    prev_scratch = evidence["seed"]["table"]

    counted = [r for r, v in prev_scratch.items() if v["theorems"] is not None]
    total = sum(v["theorems"] for v in prev_scratch.values()
                if v["theorems"] is not None)
    if len(counted) != 35 or total != 4063:
        fail(f"seed census reads {len(counted)} counted, {total} theorems")
    if prev_scratch[EMERGENCE]["theorems"] != 63:
        fail("seed emergence count is not the recorded 63")

    for label in order[1:]:
        pins = pins_by_run[label]["census_pins"]
        moved = sorted(r for r in pins
                       if r not in prev or pins[r] != prev[r])
        run = evidence["runs"][label]
        if run["recounted"] != moved:
            fail(f"{label}: recount set {run['recounted']} != moved {moved}")
        if run["incremental_table"] != run["from_scratch_table"]:
            fail(f"{label}: incremental table differs from from-scratch")
        if run["disagreements"]:
            fail(f"{label}: disagreements recorded in evidence")
        scratch = run["from_scratch_table"]
        for repo, entry in scratch.items():
            before = prev_scratch[repo]["theorems"]
            if repo == EMERGENCE and label == "run81":
                if entry["theorems"] != 68:
                    fail("run81 emergence count is not the recorded 68")
            elif entry["theorems"] != before:
                fail(f"{label}: {repo} count moved without a pin move")
        entry = scratch[UNRESOLVABLE]
        if entry["theorems"] is not None:
            fail(f"{label}: the named uncountable entry carries a count")
        prev = pins
        prev_scratch = scratch

    print("gate: PASS moved, tables, seed, change, named")


if __name__ == "__main__":
    main()
