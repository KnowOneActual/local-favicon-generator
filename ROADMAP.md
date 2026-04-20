# Roadmap

Potential features for future versions.

## v2.0.0

### Auto Theme Color
Extract dominant color from input image automatically for PWA manifest theming.

```
--auto_theme_color   # Extracts color from image
```

### Batch Processing
Process multiple source images at once.

```
python favicon_gen.py --batch input/logo.png input/icon.png --favicon_package
```

### Config File
Store default settings in `favicons.json` to avoid repeating arguments.

```json
{
  "favicon_path": "/img/favicon",
  "site_name": "My App",
  "sizes": [16, 32, 96, 180]
}
```

## v2.1.0

### Demo HTML Page
Generate a simple HTML page showing all generated favicons rendered.

### iOS/macOS icns
Generate native `.icns` for macOS.

### Windows Tiles
Generate `mstile-*` images for Windows start screen.

## v2.2.0

### Safari Pinned Tab
Generate Safari pinned tab SVG.

### Dark Mode Favicon
Generate dark variant for system dark mode.

## v3.0.0

### CLI Wizard
Interactive mode with prompts.

```
? Enter input image: input/logo.png
? Where to store favicons? [/img/favicon]
? Site name: My App
...
```

### Watch Mode
Auto-regenerate when input image changes.

```
python favicon_gen.py --watch input/logo.png --favicon_package
```

---

Priority: Auto Theme Color, Config File, Demo HTML first.