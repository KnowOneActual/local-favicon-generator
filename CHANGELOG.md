# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- Modern 2025 "Bulletproof" favicon package support.
  - SVG as primary icon for modern browsers.
  - WebP future-proof fallback support.
  - Web Application Manifest icons (192x192, 512x512) for Android/PWA.
  - 32x32 ICO legacy fallback.
- Added automatic transparency trimming (autocrop) to maximize icon visibility in browser tabs.
- Added aspect ratio preservation (padding) for non-square input images.

### Changed
- Improved SVG generation to use a square `viewBox` and center the image (prevents browser stretching).
- Updated HTML snippet to prioritize SVG and modern fallbacks, and optimized tag order.
- Simplified `favicon.ico` to a single 32x32 frame for modern systems.
- iOS icons now use the site background color for a solid fill (standard practice).

## [1.0.0] - 2024-04-20

### Added
- Initial release
- Basic image format conversion (PNG, WebP, JPEG, SVG)
- Custom size generation
- Resize with aspect ratio preservation