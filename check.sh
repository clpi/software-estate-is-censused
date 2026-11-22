#!/bin/sh
set -eu
cd "$(dirname "$0")"
if [ -d "${HOME}/workspace/tools/lean-dl/lean-4.19.0-linux/bin" ]; then
  export PATH="${HOME}/workspace/tools/lean-dl/lean-4.19.0-linux/bin:${PATH}"
else
  export PATH="${HOME}/.elan/bin:${PATH}"
fi
if find . -name '*.lean' -not -path './.lake/*' -print0 |
  xargs -0 grep -En '(^|[^[:alnum:]_])(sorry|admit|axiom|native_decide)([^[:alnum:]_]|$)'; then
  echo 'Prohibited proof escape hatch' >&2
  exit 1
fi
lake build -R -KwarningAsError=true
python3 gate.py
