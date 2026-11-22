#!/usr/bin/env python3
"""Mechanical theorem counter for the mirror strike.

Fetches every .lean blob of a repo at a pin through the gh route
(git trees API, then blob API), caches the texts under counts/, and
counts theorem declarations under a stated basis:

  basis v2: a line outside any comment whose first token is `theorem`,
  allowing leading whitespace and any run of the modifiers private /
  protected / noncomputable before it. (Basis v1, which did not strip
  comments, counted one prose line inside a block comment in
  EmergenceRung3.lean — "theorem only if rung 6's certificate ..." —
  and so read exactly one high on that repo at both calibrated pins:
  64/69 against the recorded 63/68. V2 matches the recorded census
  basis on both calibrated repos: emergence 63 and 68, the synthesis
  repo 11.)

The same function is the counting function of both the from-scratch
census and the incremental accounting; the mirror question is whether
the two agree, not whether the basis is the only possible one.
"""
import base64
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "counts")
ENV = dict(os.environ, HOME="/home/hatch", GH_CONFIG_DIR="/home/hatch/.config/gh")

THEOREM_LINE = re.compile(
    r"^\s*(?:(?:private|protected|noncomputable)\s+)*theorem\s+\S")


def gh_api(path):
    out = subprocess.run(
        ["gh", "api", path], capture_output=True, text=True, env=ENV)
    if out.returncode != 0:
        raise RuntimeError(f"gh api {path} failed: {out.stderr.strip()[:300]}")
    return json.loads(out.stdout)


def lean_texts(repo, pin):
    """Yield (path, text) for every .lean file of repo at pin."""
    cache_dir = os.path.join(CACHE, f"{repo}@{pin}")
    if os.path.isdir(cache_dir):
        for name in sorted(os.listdir(cache_dir)):
            with open(os.path.join(cache_dir, name), encoding="utf-8") as f:
                yield name, f.read()
        return
    tree = gh_api(f"repos/clpi/{repo}/git/trees/{pin}?recursive=1")
    if tree.get("truncated"):
        raise RuntimeError(f"tree truncated for {repo}@{pin}")
    paths = [t["path"] for t in tree["tree"]
             if t["type"] == "blob" and t["path"].endswith(".lean")]
    os.makedirs(cache_dir, exist_ok=True)
    for i, path in enumerate(paths):
        blob = gh_api(f"repos/clpi/{repo}/contents/{path}?ref={pin}")
        text = base64.b64decode(blob["content"]).decode("utf-8")
        flat = path.replace("/", "__")
        with open(os.path.join(cache_dir, flat), "w", encoding="utf-8") as f:
            f.write(text)
        yield path, text


def strip_comments(text):
    """Remove Lean line comments and (nested) block comments."""
    out = []
    i, n, depth = 0, len(text), 0
    while i < n:
        two = text[i:i + 2]
        if depth == 0 and two == "--":
            j = text.find("\n", i)
            i = n if j < 0 else j
        elif two == "/-":
            depth += 1
            i += 2
        elif two == "-/" and depth > 0:
            depth -= 1
            i += 2
        else:
            if depth == 0:
                out.append(text[i])
            i += 1
    return "".join(out)


def count_theorems(repo, pin):
    total = 0
    files = 0
    for _path, text in lean_texts(repo, pin):
        files += 1
        for line in strip_comments(text).splitlines():
            if THEOREM_LINE.match(line):
                total += 1
    return {"repo": repo, "pin": pin, "theorems": total, "lean_files": files}


if __name__ == "__main__":
    repo, pin = sys.argv[1], sys.argv[2]
    print(json.dumps(count_theorems(repo, pin)))
