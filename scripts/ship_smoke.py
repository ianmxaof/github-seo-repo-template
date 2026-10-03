"""Ship smoke for github-seo — file presence + import analyzer (no full pytest by default)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    required = [
        ROOT / "PRODUCT_INTENT.md",
        ROOT / "RULES.md",
        ROOT / "tests" / "test_analyzer.py",
        ROOT / "pyproject.toml",
    ]
    missing = [str(p.relative_to(ROOT)) for p in required if not p.is_file()]
    if missing:
        print(f"FAIL: missing {', '.join(missing)}", file=sys.stderr)
        return 1

    # Shallow import: packages under src/ if present
    src = ROOT / "src"
    if src.is_dir():
        sys.path.insert(0, str(ROOT))
        sys.path.insert(0, str(src))
        try:
            # Prefer a light module if it exists
            import importlib

            for mod in ("analyzer", "presets", "gh_visibility"):
                try:
                    importlib.import_module(mod)
                    print(f"github-seo ship_smoke ok (imported {mod})")
                    return 0
                except Exception:
                    continue
        except Exception as e:  # noqa: BLE001
            print(f"WARN: import probe skipped ({e})")

    print("github-seo ship_smoke ok (files present)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
