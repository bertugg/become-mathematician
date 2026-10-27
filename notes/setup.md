# Development Environment Setup (macOS)

You'll do this once. Allow about 15 minutes.

## What you already have
- Python 3.14 (Homebrew)
- `uv`, a fast Python package and environment manager
- VS Code (`code` command)

## Why `uv` + `pyproject.toml`
Slot maths has to be **reproducible**: a reviewer, QA or a test lab must get identical numbers from your code. This setup gives you that in three pieces:
- `pyproject.toml` lists the libraries the project needs.
- `uv.lock` pins the exact versions, which makes it the reproducibility record.
- `.venv/` is an isolated environment for this project only. It is not committed, and you can recreate it at any time.

This is the same principle as pinning dependencies in a frontend `package-lock.json`.

## The libraries and their roles in this course
| Library | Used for | Session |
|---|---|---|
| `fractions` (built-in) | **Exact** probabilities with no float rounding | 1–3 |
| `itertools` (built-in) | Enumerating reel-stop combinations | 2–3 |
| `numpy` | Vectorised enumeration and fast Monte Carlo | 3–5 |
| `pandas` | Paytable and RTP-contribution tables | 2–7 |
| `scipy.stats` | Confidence intervals and distributions | 4–5 |
| `matplotlib` | Payout distributions and convergence plots | 4–5 |
| `pytest` | Unit tests for the win evaluator | 3+ |
| `jupyterlab` | Exploratory notebooks and report drafts | optional |
| `ruff` | Linting and formatting | optional |

## Step 1: Create the environment
From the project folder:
```bash
cd ~/OwnWorkspace/become-mathematician
uv sync
```
This creates `.venv/` and installs everything listed in `uv.lock`.

## Step 2: Verify it works
```bash
uv run python -c "import numpy, pandas, scipy, matplotlib; print('numpy', numpy.__version__)"
uv run python -c "from fractions import Fraction as F; print(F(2,30) * F(4,30))"
```
The second command should print `2/225`. That is exact arithmetic, with no `0.00888...` rounding.

## Step 3: Create the code layout
```
ember_forge/
    __init__.py      (empty file; makes the folder an importable package)
    config.py        (Exercise 1.2: symbol counts, paytable, p_symbol)
tests/
    test_config.py   (your tests, e.g. each reel sums to 30)
notebooks/           (optional, for Jupyter)
```
```bash
mkdir -p ember_forge tests notebooks
touch ember_forge/__init__.py
```

## Step 4: Set up VS Code
```bash
code .
```
1. Install these extensions: **Python** and **Jupyter** (Microsoft), and **Ruff** (Astral).
2. Press `Cmd+Shift+P`, choose **Python: Select Interpreter**, then pick `./.venv/bin/python`.
3. In the terminal, `which python` should then point inside `.venv` (or use `uv run ...` throughout).

## Everyday commands
| Task | Command |
|---|---|
| Run a script | `uv run python -m ember_forge.config` |
| Run all tests | `uv run pytest` |
| Run tests verbosely | `uv run pytest -v` |
| Open Jupyter | `uv run jupyter lab` |
| Lint and format | `uv run ruff check .` / `uv run ruff format .` |
| Add a library | `uv add <name>` (updates pyproject + lock) |

## Step 5 (recommended): Version control
This project becomes your portfolio, and a clean git history with sensible commits is itself evidence of professional practice.
```bash
git init
git add .
git commit -m "Initial project: design brief, notes, environment"
```

## Two habits to start now
1. **Exact first, float later.** Use `Fraction` for theoretical probabilities and RTP. Switch to `float`/`numpy` only for speed (simulation, large enumeration), and compare the results against the exact values.
2. **Always seed randomness.** From Session 4, every simulation uses `rng = numpy.random.default_rng(seed)` and records its seed. An unseeded simulation can't be reproduced, so a reviewer can't check its numbers.

## Troubleshooting
- `uv: command not found`: run `brew install uv`.
- VS Code doesn't see the packages: you selected the wrong interpreter; repeat Step 4.2.
- `ModuleNotFoundError: ember_forge` in tests: run tests from the project root with `uv run pytest`.
  `pyproject.toml` already sets `pythonpath = ["."]`.
