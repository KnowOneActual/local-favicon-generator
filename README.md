# Local Favicon Generator

<p align="center">
  <img src="assets/img/logo/logo.webp" alt="Local Favicon Generator Logo" width="200" height="200">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.7+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome">
  <img src="https://img.shields.io/badge/maintained-yes-blue.svg" alt="Maintained">
</p>

Generate complete favicon packages locally — no external services required. Replicates the core functionality of [RealFaviconGenerator.net](https://realfavicongenerator.net/) entirely offline.

## Features

- **Multi-resolution ICO** — Generates favicon.ico with 16, 32, 48, and 64px sizes embedded
- **Apple Touch Icon** — 180x180px PNG for iOS home screen
- **PWA Manifest** — Generates site.webmanifest for Android/PWA support
- **HTML Snippet** — Outputs ready-to-use `<link>` tags for your `<head>`
- **Multiple Formats** — PNG, WebP, SVG output at custom sizes
- **Transparency Support** — Handles alpha channels properly

## Installation

```bash
# Recommended: Install as an editable package
pip install -e .

# Or just dependencies
pip install Pillow
```

## Quick Start

```bash
# Basic usage (using the included project logo as a test)
python favicon_gen.py input/logo.png

# Generate complete favicon package (Recommended)
python favicon_gen.py input/logo.png --favicon_package
```


## Interactive Wizard

Run without arguments for an interactive prompt:

```bash
python favicon_gen.py
```

You'll be asked for:
- Input image path
- Where to store favicons (default: `/img/favicon`)
- Site name (full and short)
- Background color

Theme color is auto-detected from your image.

## Favicon Package Output

Running with `--favicon_package` generates:

```
output/
├── favicon.ico              # Multi-resolution (16,32,48,64px)
├── favicon-32x32.png        # 32x32 PNG
├── favicon-96x96.png        # 96x96 PNG
├── favicon.svg              # SVG vector
├── favicon.webp             # WebP format
├── apple-touch-icon.png     # 180x180 for iOS
├── site.webmanifest         # PWA manifest
├── favicon-tags.html       # HTML <link> tags
└── favicon-code.txt        # Plain code to paste in your <head>
```

**favicon-code.txt** contains the `<link>` tags — just copy-paste into your HTML `<head>`:

## Usage

### Basic Image Generation

```bash
python favicon_gen.py <input_image> -o <output_dir> -f <formats> -s <sizes>
```

**Examples:**

```bash
# Default: PNG + WebP at 32x32, 96x96
python favicon_gen.py input/favicon.png

# Custom formats and sizes
python favicon_gen.py input/favicon.png -f png webp jpeg -s 32x32 96x96 180x180

# Custom output name
python favicon_gen.py input/logo.png -n logo
```

### Favicon Package Mode

```bash
python favicon_gen.py input/favicon.png --favicon_package
```

**Options:**

| Flag | Description | Default |
|------|-------------|---------|
| `--favicon_package` | Generate complete favicon package | False |
| `--favicon_path` | Path where favicons will be hosted | `/img/favicon` |
| `--site_name` | Full site name for manifest | "My Site" |
| `--short_name` | Short name for manifest | "Site" |
| `--theme_color` | Theme color (hex) | auto-extract |
| `--bg_color` | Background color (hex) | #ffffff |
| `--auto` | Auto-extract theme color from image | enabled by default |

### Custom Manifest Values

```bash
python favicon_gen.py input/favicon.png \
  --favicon_package \
  --favicon_path /img/favicon \
  --site_name "My Awesome App" \
  --short_name "App" \
  --theme_color "#1a73e8" \
  --bg_color "#ffffff"
```

### Auto Theme Color

Theme color is automatically extracted from the input image by default. Use `--auto` to be explicit or override with `--theme_color`:

```bash
# Auto-extract (default)
python favicon_gen.py input/favicon.png --favicon_package

# Explicit auto
python favicon_gen.py input/favicon.png --favicon_package --auto

# Manual override
python favicon_gen.py input/favicon.png --favicon_package --theme_color "#1a73e8"
```

## HTML Integration

Open `favicon-code.txt` — copy the lines into your `<head>`:

```html
<link rel="icon" type="image/png" href="/img/favicon/favicon-96x96.png" sizes="96x96" />
<link rel="icon" type="image/svg+xml" href="/img/favicon/favicon.svg" />
<link rel="shortcut icon" href="/img/favicon/favicon.ico" />
<link rel="apple-touch-icon" sizes="180x180" href="/img/favicon/apple-touch-icon.png" />
<link rel="manifest" href="/img/favicon/site.webmanifest" />
```

Extract the package to `<site>/img/favicon/` and update the paths as needed.

## Project Structure

```
image_generator/
├── favicon_gen.py       # Main script
├── input/                   # Source images
├── output/                  # Generated variants
└── README.md
```

## Requirements

- Python 3.7+
- Pillow 10.0+

Install via: `pip install Pillow`

## License

MIT
