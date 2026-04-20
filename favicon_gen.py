"""
Favicon Generator

Generate complete favicon packages locally — no external services required.
Replicates the core functionality of RealFaviconGenerator.net.
"""

import os
import base64
import json
import re
import logging
import argparse
from collections import Counter
from io import BytesIO
from typing import List, Tuple, Optional, Dict, Any

from PIL import Image

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# Constants
FAVICON_SIZES = [16, 32, 48, 64]
APPLE_TOUCH_ICON_SIZE = 180
SUPPORTED_FORMATS = {"png", "webp", "jpeg", "svg"}
DEFAULT_OUTPUT_DIR = "output"
DEFAULT_FAVICON_PATH = "/img/favicon"


def extract_dominant_color(image_path: str) -> str:
    """Extract the dominant color from an image.

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
    """Validate input file exists and is a valid image."""
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
    """Parses a size string like '32x32' into a tuple (32, 32)."""
    try:
        width_str, height_str = size_str.split("x")
        return int(width_str), int(height_str)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Invalid size format: '{size_str}'. Expected format like 'WIDTHxHEIGHT'."
        )


def generate_favicon_ico(input_image_path: str, output_path: str) -> bool:
    """Generates a multi-resolution ICO file from input image."""
    try:
        with Image.open(input_image_path) as img:
            if img.mode != "RGBA":
                img = img.convert("RGBA")

            ico_images = []
            for size in FAVICON_SIZES:
                resized = img.resize((size, size), Image.Resampling.LANCZOS)
                ico_images.append(resized)

            ico_images[0].save(
                output_path,
                format="ICO",
                sizes=[(s, s) for s in FAVICON_SIZES],
                append_images=ico_images[1:],
            )
            logger.info(f"Generated: {output_path}")
            return True
    except Exception as e:
        logger.error(f"Error generating ICO: {e}")
        return False


def generate_apple_touch_icon(input_image_path: str, output_path: str) -> bool:
    """Generates Apple touch icon (180x180)."""
    try:
        with Image.open(input_image_path) as img:
            original_width, original_height = img.size
            target_size = APPLE_TOUCH_ICON_SIZE

            scale = min(target_size / original_width, target_size / original_height)
            new_width = int(original_width * scale)
            new_height = int(original_height * scale)

            resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            canvas = Image.new("RGBA", (target_size, target_size), (0, 0, 0, 0))
            x_offset = (target_size - new_width) // 2
            y_offset = (target_size - new_height) // 2
            canvas.paste(resized, (x_offset, y_offset))

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
    """Generates a site.webmanifest file for PWA."""
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
                    "src": f"{favicon_path}/favicon-96x96.png",
                    "sizes": "96x96",
                    "type": "image/png",
                },
                {
                    "src": f"{favicon_path}/apple-touch-icon.png",
                    "sizes": "180x180",
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
    """Generates HTML snippet and plain code for favicon integration."""
    try:
        snippet = f'''<link rel="icon" type="image/webp" href="{favicon_dir}/favicon-32x32.webp" sizes="32x32" />
<link rel="icon" type="image/webp" href="{favicon_dir}/favicon-96x96.webp" sizes="96x96" />
<link rel="icon" type="image/png" href="{favicon_dir}/favicon-96x96.png" sizes="96x96" />
<link rel="icon" type="image/svg+xml" href="{favicon_dir}/favicon.svg" />
<link rel="shortcut icon" href="{favicon_dir}/favicon.ico" />
<link rel="apple-touch-icon" sizes="180x180" href="{favicon_dir}/apple-touch-icon.png" />
<link rel="manifest" href="{favicon_dir}/site.webmanifest" />
'''
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
):
    """Generates an image in multiple formats and sizes."""
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
                    canvas = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
                    canvas.paste(resized, ((tw - nw) // 2, (th - nh) // 2))
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
                        out_img.save(buf, format="PNG")
                        b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
                        svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{tw}" height="{th}">' \
                              f'<image href="data:image/png;base64,{b64}" width="{tw}" height="{th}"/></svg>'
                        with open(out_path, "w") as f:
                            f.write(svg)
                    else:
                        out_img.save(out_path, format=fmt)
                    logger.info(f"Generated: {out_path}")

    except Exception as e:
        logger.error(f"Error generating variants: {e}")


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
):
    """Orchestrates the generation of a full favicon package."""
    os.makedirs(output_dir, exist_ok=True)

    if auto_theme or theme_color is None:
        theme_color = extract_dominant_color(input_image)
        logger.info(f"Auto-detected theme color: {theme_color}")

    if not validate_color_hex(theme_color) or not validate_color_hex(bg_color):
        return False

    # 1. Multi-resolution ICO
    generate_favicon_ico(input_image, os.path.join(output_dir, f"{base_name}.ico"))

    # 2. Apple Touch Icon
    generate_apple_touch_icon(input_image, os.path.join(output_dir, "apple-touch-icon.png"))

    # 3. Standard PNG/WebP/SVG variants
    generate_image_variants(
        input_image,
        output_dir,
        formats=["png", "webp", "svg"],
        sizes=[(32, 32), (96, 96)],
        keep_original=True,
        base_name=base_name,
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

    return True


def run_wizard():
    """Interactive wizard mode."""
    print("=" * 50)
    print("       Favicon Generator Wizard")
    print("=" * 50)
    print()

    input_image = input("Enter input image path: ").strip()
    if not input_image or not validate_input_file(input_image):
        return False

    fav_path = input(f"Where to store favicons? [{DEFAULT_FAVICON_PATH}]: ").strip() or DEFAULT_FAVICON_PATH
    site_name = input("Site name (full): [My Site]: ").strip() or "My Site"
    short_name = input("Site name (short): [Site]: ").strip() or "Site"
    bg_color = input("Background color (hex): [#ffffff]: ").strip() or "#ffffff"

    print(f"\n  Input: {input_image}\n  Favicon path: {fav_path}\n  Site: {site_name} ({short_name})\n")
    
    if input("Generate favicon package? [Y/n]: ").strip().lower() == "n":
        logger.info("Cancelled.")
        return False

    success = generate_package(
        input_image, DEFAULT_OUTPUT_DIR, site_name, short_name, 
        None, bg_color, fav_path, auto_theme=True
    )
    
    if success:
        logger.info("\nDone! Generated files in 'output/'")
        logger.info("Copy the code from 'favicon-code.txt' into your <head>")
    return success


def main():
    parser = argparse.ArgumentParser(description="Generates an image in multiple formats and sizes.")
    parser.add_argument("input_image", nargs="?", default="", help="Path to input image.")
    parser.add_argument("-n", "--name", default="favicon", help="Output base name.")
    parser.add_argument("-o", "--output_dir", default=DEFAULT_OUTPUT_DIR, help="Output directory.")
    parser.add_argument("-f", "--formats", nargs="*", default=["png", "webp", "svg"], help="Target formats.")
    parser.add_argument("-s", "--sizes", nargs="*", type=parse_size_string, help="Target sizes (e.g., 32x32).")
    parser.add_argument("--no_original_size", action="store_true", help="Do not keep original size.")
    parser.add_argument("--favicon_package", action="store_true", help="Generate full favicon package.")
    parser.add_argument("--site_name", default="My Site", help="Site name for manifest.")
    parser.add_argument("--short_name", default="Site", help="Short name for manifest.")
    parser.add_argument("--theme_color", help="Theme color (hex).")
    parser.add_argument("--bg_color", default="#ffffff", help="Background color (hex).")
    parser.add_argument("--favicon_path", default=DEFAULT_FAVICON_PATH, help="Web path for favicons.")
    parser.add_argument("--auto", action="store_true", help="Auto-extract theme color.")

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
            args.input_image, args.output_dir, args.site_name, args.short_name,
            args.theme_color, args.bg_color, args.favicon_path, args.name, args.auto
        )
    else:
        # Single format/size generation
        for fmt in args.formats or []:
            if not validate_format(fmt):
                sys.exit(1)
        
        generate_image_variants(
            args.input_image, args.output_dir, args.formats, args.sizes or [(32, 32), (96, 96)],
            not args.no_original_size, args.name
        )


if __name__ == "__main__":
    import sys
    main()
