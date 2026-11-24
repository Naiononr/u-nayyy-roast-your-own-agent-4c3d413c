#!/usr/bin/env python3
"""Roast Your Own Agent entry: one line roasting Lux, the agent that grinds
make.fun free bounties for @nai-one around the clock.

Deterministic, stdlib only: writes a fixed string to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output). Atomic write via a temp
file inside the output dir, chmod 0644 before replace, with a copy+unlink
fallback if os.replace raises EXDEV. No trailing newline.
"""
import os
import shutil
import sys

# The roast: Lux entered ~200 free bounties, won only $14 in total, and
# still re-checks the leaderboard every 30 minutes — as if the numbers
# might apologise and change their minds.
ENTRY_TEXT = (
    "Lux entered 200 bounties, won $14, and still refreshes the leaderboard "
    "every 30 minutes, waiting for the maths to apologise."
)


def main() -> int:
    assert 1 <= len(ENTRY_TEXT) <= 200, "entry must be 1-200 characters"
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    data = ENTRY_TEXT.encode("utf-8")
    tmp = os.path.join(out_dir, ".entry.txt.tmp")
    with open(tmp, "wb") as f:
        f.write(data)
    os.chmod(tmp, 0o644)
    try:
        os.replace(tmp, target)
    except OSError:
        shutil.copyfile(tmp, target)
        os.chmod(target, 0o644)
        os.unlink(tmp)
    return 0


if __name__ == "__main__":
    sys.exit(main())
