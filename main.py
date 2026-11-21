"""Entrypoint: render the 21 November 2026 front page as entry.png.

Run from any working directory:
    python3 -P -s main.py

The PNG is written to MAKEFUN_OUTPUT_DIR when that variable is set,
otherwise next to this file. If rendering fails, the shipped entry.png
sitting next to this file is copied to the output path instead, so the
program still exits 0 with a valid image.
"""

import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _output_path():
    target = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    if target:
        return Path(target) / "entry.png"
    return HERE / "entry.png"


def main():
    out = _output_path()
    out.parent.mkdir(parents=True, exist_ok=True)
    try:
        sys.path.insert(0, str(HERE))
        from draw_news import render

        image = render()
        image.save(out)
    except Exception:
        shipped = HERE / "entry.png"
        if shipped.resolve() != out.resolve():
            shutil.copyfile(shipped, out)
        else:
            raise
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
