#!/usr/bin/env python3
"""Mirror strike: incremental estate accounting beside the closed-loop runs.

State: per repo, a basis triple (census pin, theorem count, counting
basis name). The counting function is count.count_theorems (basis v2),
shared by both mechanisms — the mirror question is whether maintaining
the accounting incrementally reproduces the from-scratch census, not
whether the basis is the only possible one.

From-scratch census at a run: apply the counting function to every
repo at that run's census pins (synthesis-pins.json as recorded at the
run's closing commit of clpi/software-is-a-closed-loop).

Incremental accounting: seeded with the from-scratch census at the
seed run's close (run 80). At each later run, a repo's count is
re-derived only when its census pin moved, it is new, or it left;
every other repo's triple is carried untouched.

Output: evidence.json with both tables per run, the recount set per
run, and every disagreement, if any.
"""
import json
import os

from count import count_theorems

HERE = os.path.dirname(os.path.abspath(__file__))
BASIS = "declaration lines outside comments, basis v2 (count.py)"

_count_cache = {}

# Repos whose tree cannot be fetched at their census pin at all, with
# the reason. The counting function is unexecutable for these on both
# mechanisms alike: the from-scratch census cannot recount them, and
# the incremental accounting carries them. They are reported as named
# exclusions, never silently dropped and never counted as agreement
# on a number.
UNRESOLVABLE = {
    "software-is-incrementally-safe-content-branch":
        "repo does not resolve on GitHub at its census pin "
        "(gh: could not resolve to a repository); the pin never moves "
        "in the window, so both mechanisms carry the entry uncounted",
}


def C(repo, pin):
    if repo in UNRESOLVABLE:
        return None
    key = (repo, pin)
    if key not in _count_cache:
        _count_cache[key] = count_theorems(repo, pin)["theorems"]
    return _count_cache[key]


def from_scratch(pins):
    return {repo: {"pin": pin, "theorems": C(repo, pin), "basis": BASIS}
            for repo, pin in sorted(pins.items())}


def incremental_step(state, pins):
    new_state = {}
    recounted, carried, dropped = [], [], []
    for repo, pin in sorted(pins.items()):
        old = state.get(repo)
        if old is not None and old["pin"] == pin:
            new_state[repo] = old
            carried.append(repo)
        else:
            new_state[repo] = {"pin": pin, "theorems": C(repo, pin),
                               "basis": BASIS}
            recounted.append(repo)
    for repo in state:
        if repo not in pins:
            dropped.append(repo)
    return new_state, {"recounted": recounted, "carried": carried,
                       "dropped": dropped}


def main():
    with open(os.path.join(HERE, "pins.json")) as f:
        pins_by_run = json.load(f)
    order = ["seed", "run81", "run82", "run83", "run84"]
    registered = ["run81", "run82", "run83"]  # the three consecutive runs
    evidence = {"basis": BASIS, "runs": {}}
    state = from_scratch(pins_by_run["seed"]["census_pins"])
    evidence["seed"] = {"commit": pins_by_run["seed"]["commit"],
                        "table": state}
    for label in order[1:]:
        pins = pins_by_run[label]["census_pins"]
        scratch = from_scratch(pins)
        state, step = incremental_step(state, pins)
        disagreements = []
        for repo in sorted(set(scratch) | set(state)):
            a, b = scratch.get(repo), state.get(repo)
            if a != b:
                disagreements.append(
                    {"repo": repo, "from_scratch": a, "incremental": b})
        evidence["runs"][label] = {
            "commit": pins_by_run[label]["commit"],
            "registered_window": label in registered,
            "repos_compared": len(scratch),
            "recounted": step["recounted"],
            "carried": len(step["carried"]),
            "dropped": step["dropped"],
            "disagreements": disagreements,
            "incremental_table": state,
            "from_scratch_table": scratch,
        }
        print(f"{label}: compared {len(scratch)} repos, "
              f"recounted {step['recounted']}, carried {len(step['carried'])}, "
              f"disagreements {len(disagreements)}")
    with open(os.path.join(HERE, "evidence.json"), "w") as f:
        json.dump(evidence, f, indent=1)
    print("evidence.json written")


if __name__ == "__main__":
    main()
