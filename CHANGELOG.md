# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- Complete favicon package generation (`--favicon_package`)
  - Multi-resolution ICO (16, 32, 48, 64px embedded in one file)
  - Apple Touch Icon (180x180px for iOS)
  - PWA site.webmanifest with customizable name, colors
  - HTML favicon tags for `<head>` insertion
- `--favicon_path` argument to specify favicon storage path (default: `/img/favicon`)
- `--site_name`, `--short_name`, `--theme_color`, `--bg_color` for PWA manifest customization
- `favicon-code.txt` — plain text file with `<link>` tags ready to copy-paste
- WebP format output (32x32, 96x96) alongside PNG
- Input validation with helpful error messages
- Color hex validation
- Auto theme color extraction from input image (`--auto`)
  - Uses dominant color algorithm for accurate matching
  - Runs by default when using `--favicon_package`
- Interactive CLI wizard mode
  - Runs automatically when no arguments provided
  - Prompts for input image, favicon path, site name, colors
  - Auto-detects theme color from image

### Changed
- Default formats now include `svg` in addition to `png` and `webp`
- Output paths now use relative paths from web root in HTML/code files

### Fixed
- Transparency handling for proper alpha channel support

## [1.0.0] - 2024-04-20

### Added
- Initial release
- Basic image format conversion (PNG, WebP, JPEG, SVG)
- Custom size generation
- Resize with aspect ratio preservation