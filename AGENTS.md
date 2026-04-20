# AGENTS.md

## Run

```bash
python favicon_gen.py <input_image> -o <output_dir> -f <formats> -s <sizes>
```

Examples:
```bash
# Default: png + webp at original size
python favicon_gen.py input/favicon.png

# Custom formats and sizes
python favicon_gen.py input/favicon.png -o output -f png webp jpeg -s 32x32 96x96
```

## Dependencies

Requires Pillow: `pip install Pillow`

## Structure

- `input/` — source images
- `output/` — generated variants (e.g., `favicon-32x32.png`, `favicon.webp`)
- `.venv/` or `venv/` — Python virtual environments (use either, both work)

## Notes

- JPEG output automatically converts RGBA/LA to RGB
- Default quality: webp=80, jpeg=85
- No tests, CI, or build system to maintain