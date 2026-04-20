# GEMINI.md: Local Favicon Generator

## Project Overview
**Local Favicon Generator** is a professional-grade, Python-based CLI tool for generating high-quality favicon packages and multi-format image variants locally. It replicates the functionality of RealFaviconGenerator.net, ensuring privacy and offline reliability.

- **Primary Technologies:** Python 3.7+, Pillow (PIL) 12.2+.
- **Architecture:** 
  - Modular CLI design with a core orchestration engine (`generate_package`).
  - Integrated interactive Wizard for low-friction setup.
  - Robust validation and automated dominant color extraction.

## Building and Running
### Environment Setup
The project follows standard Python packaging conventions.

```bash
# Recommended: Use the existing virtual environment
source .venv/bin/activate

# Install in editable mode
pip install -e .
```

### Key Commands
- **Interactive Wizard:** Run without arguments to start the interactive prompt.
  ```bash
  python favicon_gen.py
  ```
- **Complete Favicon Package (using project logo):**
  ```bash
  python favicon_gen.py input/logo.png --favicon_package
  ```
- **Custom Image Generation:**
  ```bash
  python favicon_gen.py input/logo.png -f png webp jpeg -s 32x32 96x96 180x180
  ```
- **Auto Theme Color Extraction:**
  ```bash
  python favicon_gen.py input/logo.png --favicon_package --auto
  ```

## Development Conventions
- **Directory Structure:**
  - `assets/img/logo/`: Project brand assets.
  - `input/`: Default directory for source images (e.g., `logo.png`).
  - `output/`: Default directory for generated assets.

