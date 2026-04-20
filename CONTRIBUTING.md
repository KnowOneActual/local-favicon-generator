# Contributing to Local Favicon Generator

Thank you for your interest in improving the **Local Favicon Generator**! Your help is welcome and greatly appreciated.

## Getting Started

### 1. Prerequisites
- Python 3.7+
- [uv](https://github.com/astral-sh/uv) (recommended) or `pip`

### 2. Development Setup
Clone the repository and install it in editable mode with development dependencies:

```bash
git clone https://github.com/your-username/local-favicon-generator.git
cd local-favicon-generator
python -m venv .venv
source .venv/bin/activate
pip install -e .
pip install pytest
```

## How to Contribute

### Reporting Bugs
If you find a bug, please open an issue with:
- A clear, descriptive title.
- Steps to reproduce the bug.
- A description of the expected and actual behavior.
- Details about your environment (OS, Python version, Pillow version).

### Suggesting Enhancements
New features are welcome! Please check the `ROADMAP.md` before suggesting a new feature to see if it's already planned.

### Pull Requests
1.  **Fork the repo** and create your branch from `main`.
2.  **Add tests** for any new functionality or bug fixes.
3.  **Run tests** using `pytest`:
    ```bash
    export PYTHONPATH=.
    pytest tests/test_favicon_gen.py
    ```
4.  **Follow PEP 8** coding standards.
5.  **Keep it modular**: Ensure your changes integrate naturally into the existing `favicon_gen.py` architecture.
6.  **Update documentation** (README, GEMINI.md) if you add new features or change CLI arguments.

## Coding Standards
- Use **Type Hints** for all new functions.
- Prefer **Logging** over `print()` for console output.
- Write clear, concise docstrings for all public methods and modules.
- Ensure `pyproject.toml` is updated if new dependencies are introduced.

## Questions?
Feel free to open an issue for discussion!
