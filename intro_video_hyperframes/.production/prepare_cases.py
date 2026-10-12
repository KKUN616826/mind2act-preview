from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".production/source-refresh-20261010-142512/build-feature-cases.py"


if __name__ == "__main__":
    raise SystemExit(subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT).returncode)
