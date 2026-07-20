"""Run the full test suite: cross-file validation, number sync, browser tests.

Run:  python tests/run_all.py
Exits nonzero if any suite fails. See each script's docstring for its
dependencies; browser tests are skipped with a warning if playwright is
not installed.
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SUITES = ["validate_all.py", "sync_check.py", "test_site.py"]


def main():
    failures = []
    for suite in SUITES:
        print(f"\n=== {suite} ===")
        if suite == "test_site.py":
            try:
                import playwright  # noqa: F401
            except ImportError:
                print("playwright not installed; browser tests skipped")
                continue
        rc = subprocess.run([sys.executable, str(HERE / suite)]).returncode
        if rc != 0:
            failures.append(suite)
    print("\n=== summary ===")
    if failures:
        print("FAILED:", ", ".join(failures))
    else:
        print("all suites passed")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
