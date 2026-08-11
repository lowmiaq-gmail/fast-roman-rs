#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
python_bin=${PYTHON:-python3}

"$python_bin" - <<'PY'
import os
import roman

expected = os.environ.get("CANDIDATE_EXPECTED_ROOT")
actual = os.path.realpath(roman.__file__)
if expected and not actual.startswith(os.path.realpath(expected)):
    raise SystemExit("candidate import escaped expected root: %s" % actual)
print("candidate import:", actual)
PY

cd "$repo_root"
"$python_bin" -m unittest discover -s upstream/tests -p tests.py -v
