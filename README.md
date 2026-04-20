<p align="center">
  <img src="assets/img/logo/logo.webp" alt="Local Favicon Generator Logo" width="200" height="200">
</p>

# Local Favicon Generator

<p align="center">
  <img src="https://img.shields.io/badge/python-3.7+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome">
  <img src="https://img.shields.io/badge/maintained-yes-blue.svg" alt="Maintained">
</p>

Generate complete favicon packages locally: no external services required. Follows modern 2025 best practices (SVG primary, PNG/WebP fallbacks, PWA support) entirely offline. Similar to how [Real Favicon Generator.net](https://realfavicongenerator.net) functions. 

## Features

- **SVG Primary** — Scalable vector icon for modern browsers (Chrome, Firefox, Edge)
- **Autocrop (Trim)** — Automatically removes transparent borders to ensure your icon fills the tab (no more "stumpy" icons)
- **Modern Fallbacks** — 32x32 PNG and WebP for broad compatibility
- **Apple Touch Icon** — 180x180px solid PNG for iOS home screen
- **PWA Manifest** — Generates site.webmanifest with 192px and 512px icons for Android/PWA
- **Legacy ICO** — 32x32 ICO fallback for legacy tools
- **HTML Snippet** — Outputs a modern "Bulletproof" `<link>` tag set
- **Transparency Support** — Intelligent handling (solid for iOS, transparent for desktop)

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
├── favicon.svg              # Primary vector icon
├── favicon.ico              # 32x32 legacy fallback
├── favicon-32x32.png        # Standard PNG fallback
├── favicon-32x32.webp       # Future-proof WebP fallback
├── apple-touch-icon.png     # 180x180 solid for iOS
├── web-app-manifest-192x192.png # Android home screen
├── web-app-manifest-512x512.png # PWA splash screen
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
<link rel="icon" type="image/svg+xml" href="/img/favicon/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/img/favicon/favicon-32x32.png">
<link rel="icon" type="image/webp" sizes="32x32" href="/img/favicon/favicon-32x32.webp">
<link rel="alternate icon" href="/img/favicon/favicon.ico">
<link rel="manifest" href="/img/favicon/site.webmanifest">
<link rel="apple-touch-icon" href="/img/favicon/apple-touch-icon.png">
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
