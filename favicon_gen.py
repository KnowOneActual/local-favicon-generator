"""Favicon Generator.

Generate complete favicon packages locally — no external services required.
Replicates the core functionality of RealFaviconGenerator.net.
"""

import argparse
import base64
import json
import logging
import os
import re
from collections import Counter
from io import BytesIO
from typing import List, Optional, Tuple

from PIL import Image

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# Constants
FAVICON_SIZES = [32]  # Standard fallback size for modern ICO
APPLE_TOUCH_ICON_SIZE = 180
ANDROID_ICON_SIZES = [192, 512]
SUPPORTED_FORMATS = {"png", "webp", "jpeg", "svg"}
DEFAULT_OUTPUT_DIR = "output"
DEFAULT_FAVICON_PATH = "/img/favicon"


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert a hex color string to an RGB tuple."""
    hex_color = hex_color.lstrip("#")
    return (
        tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore
    )


def extract_dominant_color(image_path: str) -> str:
    """Extract dominant color from an image.

    Args:
        image_path: Path to the input image.

    Returns:
        Hex color string (e.g., "#ff0000").

    """
    try:
        with Image.open(image_path) as img:
            img = img.convert("RGB")
            img = img.resize((50, 50), Image.Resampling.LANCZOS)
            pixels = list(img.get_flattened_data())
            color_counts = Counter(pixels)
            dominant = color_counts.most_common(1)[0][0]
            return f"#{dominant[0]:02x}{dominant[1]:02x}{dominant[2]:02x}"
    except Exception as e:
        logger.debug(f"Failed to extract color: {e}")
        return "#ffffff"


def validate_input_file(path: str) -> bool:
    """Validate that input file exists and is a valid image."""
    if not path:
        logger.error("Error: No input image specified.")
        return False
    if not os.path.exists(path):
        logger.error(f"Error: Input file not found: {path}")
        return False
    try:
        with Image.open(path) as img:
            img.verify()
        return True
    except Exception:
        logger.error(f"Error: Cannot read image file: {path}")
        logger.error("  Supported formats: PNG, JPEG, WebP, BMP, GIF")
        return False


def validate_color_hex(color: str) -> bool:
    """Validate hex color format."""
    if not color:
        return False
    pattern = r"^#?[0-9A-Fa-f]{6}$"
    if not re.match(pattern, color):
        logger.error(f"Error: Invalid color format: {color}")
        logger.error("  Expected: #RRGGBB (e.g., #ffffff)")
        return False
    return True


def validate_format(fmt: str) -> bool:
    """Validate output format."""
    if fmt.lower() in SUPPORTED_FORMATS:
        return True
    logger.error(f"Error: Unsupported format '{fmt}'")
    logger.error(f"  Supported: {', '.join(SUPPORTED_FORMATS)}")
    return False


def parse_size_string(size_str: str) -> Tuple[int, int]:
    """Parse a size string like '32x32' into a tuple (32, 32)."""
    try:
        width_str, height_str = size_str.split("x")
        return int(width_str), int(height_str)
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Invalid size format: '{size_str}'. "
            "Expected format like 'WIDTHxHEIGHT'."
        )


def generate_favicon_ico(
    input_image_path: str,
    output_path: str,
    background_color: Tuple[int, int, int, int] = (0, 0, 0, 0),
) -> bool:
    """Generate a multi-resolution ICO file from input image."""
    try:
        with Image.open(input_image_path) as img:
            if img.mode != "RGBA":
                img = img.convert("RGBA")

            ico_images = []
            for size in FAVICON_SIZES:
                # Preserve aspect ratio and pad with background color
                original_width, original_height = img.size
                scale = min(size / original_width, size / original_height)
                new_width = int(original_width * scale)
                new_height = int(original_height * scale)

                resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                canvas = Image.new("RGBA", (size, size), background_color)
                x_offset = (size - new_width) // 2
                y_offset = (size - new_height) // 2
                canvas.paste(
                    resized, (x_offset, y_offset), resized
                )  # Use resized as mask for proper blending

                ico_images.append(canvas)

            ico_images[0].save(
                output_path,
                format="ICO",
                append_images=ico_images[1:],
            )
            logger.info(f"Generated: {output_path}")
            return True
    except Exception as e:
        logger.error(f"Error generating ICO: {e}")
        return False


def generate_apple_touch_icon(
    input_image_path: str,
    output_path: str,
    background_color: Tuple[int, int, int, int] = (0, 0, 0, 0),
) -> bool:
    """Generate Apple touch icon (180x180)."""
    try:
        with Image.open(input_image_path) as img:
            if img.mode != "RGBA":
                img = img.convert("RGBA")
            original_width, original_height = img.size
            target_size = APPLE_TOUCH_ICON_SIZE

            scale = min(target_size / original_width, target_size / original_height)
            new_width = int(original_width * scale)
            new_height = int(original_height * scale)

            resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            canvas = Image.new("RGBA", (target_size, target_size), background_color)
            x_offset = (target_size - new_width) // 2
            y_offset = (target_size - new_height) // 2
            canvas.paste(
                resized, (x_offset, y_offset), resized
            )  # Use resized as mask for proper blending

            canvas.save(output_path, format="PNG")
            logger.info(f"Generated: {output_path}")
            return True
    except Exception as e:
        logger.error(f"Error generating Apple touch icon: {e}")
        return False


def generate_site_webmanifest(
    output_path: str,
    site_name: str = "My Site",
    short_name: str = "Site",
    theme_color: str = "#ffffff",
    background_color: str = "#ffffff",
    favicon_path: str = DEFAULT_FAVICON_PATH,
) -> bool:
    """Generate a site.webmanifest file for PWA."""
    try:
        manifest = {
            "name": site_name,
            "short_name": short_name,
            "description": site_name,
            "start_url": "/",
            "display": "standalone",
            "background_color": background_color,
            "theme_color": theme_color,
            "icons": [
                {
                    "src": f"{favicon_path}/web-app-manifest-192x192.png",
                    "sizes": "192x192",
                    "type": "image/png",
                },
                {
                    "src": f"{favicon_path}/web-app-manifest-512x512.png",
                    "sizes": "512x512",
                    "type": "image/png",
                },
            ],
        }
        with open(output_path, "w") as f:
            json.dump(manifest, f, indent=2)
        logger.info(f"Generated: {output_path}")
        return True
    except Exception as e:
        logger.error(f"Error generating webmanifest: {e}")
        return False


def generate_html_metadata(
    output_dir: str, favicon_dir: str = DEFAULT_FAVICON_PATH
) -> bool:
    """Generate HTML snippet following modern 2025 best practices."""
    try:
        # 1. SVG is the primary modern format (scalable, dark mode support)
        # 2. PNG 32x32 is the reliable fallback for most browsers
        # 3. ICO is the legacy fallback
        # 4. WebP is included for future-proofing as requested
        snippet = (
            f'<link rel="icon" type="image/svg+xml" '
            f'href="{favicon_dir}/favicon.svg">\n'
            f'<link rel="icon" type="image/png" sizes="32x32" '
            f'href="{favicon_dir}/favicon-32x32.png">\n'
            f'<link rel="icon" type="image/webp" sizes="32x32" '
            f'href="{favicon_dir}/favicon-32x32.webp">\n'
            f'<link rel="alternate icon" href="{favicon_dir}/favicon.ico">\n'
            f'<link rel="manifest" href="{favicon_dir}/site.webmanifest">\n'
            f'<link rel="apple-touch-icon" '
            f'href="{favicon_dir}/apple-touch-icon.png">\n'
        )
        # Write HTML snippet
        with open(os.path.join(output_dir, "favicon-tags.html"), "w") as f:
            f.write(snippet)

        # Write Plain text code
        with open(os.path.join(output_dir, "favicon-code.txt"), "w") as f:
            f.write(snippet)

        logger.info(f"Generated HTML metadata in {output_dir}")
        return True
    except Exception as e:
        logger.error(f"Error generating HTML metadata: {e}")
        return False


def generate_image_variants(
    input_image_path: str,
    output_dir: str,
    formats: Optional[List[str]] = None,
    sizes: Optional[List[Tuple[int, int]]] = None,
    keep_original: bool = True,
    base_name: str = "favicon",
    background_color: Tuple[int, int, int, int] = (
        0,
        0,
        0,
        0,
    ),  # Default to transparent
):
    """Generate an image in multiple formats and sizes."""
    formats = formats or ["png", "webp", "svg"]
    os.makedirs(output_dir, exist_ok=True)

    try:
        with Image.open(input_image_path) as img:
            if img.mode != "RGBA":
                img = img.convert("RGBA")
            orig_w, orig_h = img.size

            target_sizes = []
            if keep_original:
                target_sizes.append((orig_w, orig_h))
            if sizes:
                for s in sizes:
                    if s not in target_sizes:
                        target_sizes.append(s)

            for tw, th in target_sizes:
                if (tw, th) != (orig_w, orig_h):
                    scale = min(tw / orig_w, th / orig_h)
                    nw, nh = int(orig_w * scale), int(orig_h * scale)
                    resized = img.resize((nw, nh), Image.Resampling.LANCZOS)
                    canvas = Image.new("RGBA", (tw, th), background_color)
                    canvas.paste(
                        resized, ((tw - nw) // 2, (th - nh) // 2), resized
                    )  # Use resized as mask
                    out_img = canvas
                    suffix = f"-{tw}x{th}"
                else:
                    out_img = img.copy()
                    suffix = ""

                for fmt in formats:
                    out_path = os.path.join(output_dir, f"{base_name}{suffix}.{fmt}")

                    if fmt == "webp":
                        out_img.save(out_path, format=fmt, quality=80)
                    elif fmt == "jpeg":
                        out_img.convert("RGB").save(out_path, format=fmt, quality=85)
                    elif fmt == "svg":
                        buf = BytesIO()
                        # Ensure we use an RGBA version for the PNG inside SVG
                        temp_img = out_img
                        if temp_img.mode != "RGBA":
                            temp_img = temp_img.convert("RGBA")
                        temp_img.save(buf, format="PNG")
                        b64 = base64.b64encode(buf.getvalue()).decode("utf-8")

                        # Use a square viewBox and center the image to prevent browser stretching
                        max_dim = max(tw, th)
                        x_off = (max_dim - tw) // 2
                        y_off = (max_dim - th) // 2

                        svg = (
                            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {max_dim} {max_dim}">'
                            f'<image href="data:image/png;base64,{b64}" x="{x_off}" y="{y_off}" width="{tw}" height="{th}"/></svg>'
                        )
                        with open(out_path, "w") as f:
                            f.write(svg)
                    else:
                        out_img.save(out_path, format=fmt)
                    logger.info(f"Generated: {out_path}")

    except Exception as e:
        logger.error(f"Error generating variants: {e}")


def trim_image(img: Image.Image) -> Image.Image:
    """Trim transparent borders from an image."""
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    bbox = img.getbbox()
    if bbox:
        return img.crop(bbox)
    return img


def generate_package(
    input_image: str,
    output_dir: str,
    site_name: str,
    short_name: str,
    theme_color: Optional[str],
    bg_color: str,
    favicon_path: str,
    base_name: str = "favicon",
    auto_theme: bool = False,
    trim: bool = True,
):
    """Orchestrate the generation of a full favicon package."""
    os.makedirs(output_dir, exist_ok=True)

    # Process source image (trim transparency to avoid "stumpy" icons)
    working_image_path = input_image
    if trim:
        try:
            with Image.open(input_image) as img:
                trimmed = trim_image(img)
                working_image_path = os.path.join(output_dir, "_tmp_trimmed_source.png")
                trimmed.save(working_image_path)
                logger.info("Trimmed transparent borders from source image.")
        except Exception as e:
            logger.warning(f"Failed to trim image: {e}. Proceeding with original.")

    if auto_theme or theme_color is None:
        theme_color = extract_dominant_color(working_image_path)
        logger.info(f"Auto-detected theme color: {theme_color}")

    if not validate_color_hex(theme_color) or not validate_color_hex(bg_color):
        return False

    # Convert bg_color hex to RGBA tuple for image generation
    bg_rgb = hex_to_rgb(bg_color)
    bg_rgba = bg_rgb + (255,)  # Add full opacity

    # 1. Multi-resolution ICO - Fallback (Transparent)
    generate_favicon_ico(
        working_image_path, os.path.join(output_dir, f"{base_name}.ico"), (0, 0, 0, 0)
    )

    # 2. Apple Touch Icon - Solid background (Standard for iOS)
    generate_apple_touch_icon(
        working_image_path, os.path.join(output_dir, "apple-touch-icon.png"), bg_rgba
    )

    # 3. Standard PNG variants (Transparent)
    generate_image_variants(
        working_image_path,
        output_dir,
        formats=["png"],
        sizes=[(32, 32)],
        keep_original=False,
        base_name=base_name,
        background_color=(0, 0, 0, 0),
    )

    # 4. Future-proof WebP variants (Transparent)
    generate_image_variants(
        working_image_path,
        output_dir,
        formats=["webp"],
        sizes=[(32, 32)],
        keep_original=False,
        base_name=base_name,
        background_color=(0, 0, 0, 0),
    )

    # 5. Web Manifest Icons (Solid background)
    generate_image_variants(
        working_image_path,
        output_dir,
        formats=["png"],
        sizes=[(192, 192), (512, 512)],
        keep_original=False,
        base_name="web-app-manifest",
        background_color=bg_rgba,
    )

    # 6. SVG (Vector)
    # Re-use existing variants logic to generate the SVG
    generate_image_variants(
        working_image_path,
        output_dir,
        formats=["svg"],
        sizes=[],
        keep_original=True,
        base_name=base_name,
        background_color=(0, 0, 0, 0),
    )

    # 4. Manifest
    generate_site_webmanifest(
        os.path.join(output_dir, "site.webmanifest"),
        site_name,
        short_name,
        theme_color,
        bg_color,
        favicon_path,
    )

    # 5. HTML Code
    generate_html_metadata(output_dir, favicon_path)

    # Cleanup temp trimmed image
    if trim and os.path.exists(working_image_path):
        os.remove(working_image_path)

    return True


def run_wizard():
    """Run the interactive wizard mode for favicon generation."""
    print("=" * 50)
    print("       Favicon Generator Wizard")
    print("=" * 50)
    print()

    input_image = input("Enter input image path: ").strip()
    if not input_image or not validate_input_file(input_image):
        return False

    fav_path = (
        input(f"Where to store favicons? [{DEFAULT_FAVICON_PATH}]: ").strip()
        or DEFAULT_FAVICON_PATH
    )
    site_name = input("Site name (full): [My Site]: ").strip() or "My Site"
    short_name = input("Site name (short): [Site]: ").strip() or "Site"
    bg_color = input("Background color (hex): [#ffffff]: ").strip() or "#ffffff"

    print(
        f"\n  Input: {input_image}\n  Favicon path: {fav_path}\n  Site: {site_name} ({short_name})\n"
    )

    if input("Generate favicon package? [Y/n]: ").strip().lower() == "n":
        logger.info("Cancelled.")
        return False

    success = generate_package(
        input_image,
        DEFAULT_OUTPUT_DIR,
        site_name,
        short_name,
        None,
        bg_color,
        fav_path,
        auto_theme=True,
        trim=True,
    )

    if success:
        logger.info("\nDone! Generated files in 'output/'")
        logger.info("Copy the code from 'favicon-code.txt' into your <head>")
    return success


def main():
    """Parse arguments and run the favicon generator.

    This function sets up the command-line argument parser,
    handles the interactive wizard mode if no arguments are provided,
    validates the input image, and then calls the appropriate
    favicon generation function (`generate_package` or `generate_image_variants`)
    based on the parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Generate an image in multiple formats and sizes for favicons."
        )
    )
    parser.add_argument(
        "input_image",
        nargs="?",
        default="",
        help="Path to input image.",
    )
    parser.add_argument(
        "-n",
        "--name",
        default="favicon",
        help="Base name for output files.",
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        default=DEFAULT_OUTPUT_DIR,
        help="Directory to save generated files.",
    )
    parser.add_argument(
        "-f",
        "--formats",
        nargs="*",
        default=["png", "webp", "svg"],
        help="Output formats.",
    )
    parser.add_argument(
        "-s",
        "--sizes",
        nargs="*",
        type=parse_size_string,
        help="Sizes (e.g., 32x32).",
    )
    parser.add_argument(
        "--no_original_size",
        action="store_true",
        help="No original size variant.",
    )
    parser.add_argument(
        "--favicon_package",
        action="store_true",
        help="Generate full package.",
    )
    parser.add_argument(
        "--site_name",
        default="My Site",
        help="Site name (full).",
    )
    parser.add_argument(
        "--short_name",
        default="Site",
        help="Short site name for the web manifest.",
    )
    parser.add_argument(
        "--theme_color",
        help="Theme color (hex). Auto-detected if omitted.",
    )
    parser.add_argument(
        "--bg_color",
        default="#ffffff",
        help="Background color in hex (e.g., #ffffff).",
    )
    parser.add_argument(
        "--favicon_path",
        default=DEFAULT_FAVICON_PATH,
        help="Web path where favicons will be hosted.",
    )
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Automatically extract dominant color for theme if not specified.",
    )
    parser.add_argument(
        "--no_trim",
        action="store_false",
        dest="trim",
        default=True,
        help="No trim transparent borders.",
    )

    if len(sys.argv) == 1:
        run_wizard()
        return

    args = parser.parse_args()

    if not args.input_image:
        args.input_image = input("Enter the path to the input image file: ").strip()

    if not validate_input_file(args.input_image):
        sys.exit(1)

    if args.favicon_package:
        generate_package(
            args.input_image,
            args.output_dir,
            args.site_name,
            args.short_name,
            args.theme_color,
            args.bg_color,
            args.favicon_path,
            args.name,
            args.auto,
            args.trim,
        )
    else:
        # Single format/size generation
        for fmt in args.formats or []:
            if not validate_format(fmt):
                sys.exit(1)

        generate_image_variants(
            args.input_image,
            args.output_dir,
            args.formats,
            args.sizes or [(32, 32), (96, 96)],
            not args.no_original_size,
            args.name,
        )


if __name__ == "__main__":
    import sys

    main()
