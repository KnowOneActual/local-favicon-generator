import os
import shutil

import pytest
from PIL import Image

import favicon_gen

# Test configuration
TEST_INPUT = "tests/test_input.png"
TEST_OUTPUT_DIR = "tests/test_output"


@pytest.fixture(scope="module", autouse=True)
def setup_teardown():
    """Set up test environment and tear down test artifacts."""
    # Setup
    os.makedirs("tests", exist_ok=True)
    img = Image.new("RGBA", (100, 100), (255, 0, 0, 255))
    img.save(TEST_INPUT)

    yield

    # Teardown - Only delete test artifacts, NOT the tests folder itself
    if os.path.exists(TEST_INPUT):
        os.remove(TEST_INPUT)
    if os.path.exists(TEST_OUTPUT_DIR):
        shutil.rmtree(TEST_OUTPUT_DIR)


def test_extract_dominant_color():
    """Test dominant color extraction."""
    color = favicon_gen.extract_dominant_color(TEST_INPUT)
    assert color.startswith("#")
    assert len(color) == 7
    # Since we created a red image, it should detect red
    assert color.lower() == "#ff0000"


def test_validate_input_file():
    """Test input file validation."""
    assert favicon_gen.validate_input_file(TEST_INPUT) is True
    assert favicon_gen.validate_input_file("non_existent.png") is False


def test_validate_color_hex():
    """Test hex color validation."""
    assert favicon_gen.validate_color_hex("#ffffff") is True
    assert favicon_gen.validate_color_hex("white") is False
    assert favicon_gen.validate_color_hex("#fff") is False  # It expects 6 chars


def test_generate_favicon_ico():
    """Test ICO favicon generation."""
    out_path = os.path.join(TEST_OUTPUT_DIR, "favicon.ico")
    os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)
    assert favicon_gen.generate_favicon_ico(TEST_INPUT, out_path) is True
    assert os.path.exists(out_path)


def test_generate_apple_touch_icon():
    """Test Apple touch icon generation."""
    out_path = os.path.join(TEST_OUTPUT_DIR, "apple-touch-icon.png")
    os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)
    assert favicon_gen.generate_apple_touch_icon(TEST_INPUT, out_path) is True
    assert os.path.exists(out_path)
    with Image.open(out_path) as img:
        assert img.size == (180, 180)


def test_generate_site_webmanifest():
    """Test site webmanifest generation."""
    out_path = os.path.join(TEST_OUTPUT_DIR, "site.webmanifest")
    os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)
    assert favicon_gen.generate_site_webmanifest(out_path) is True
    assert os.path.exists(out_path)


def test_generate_package():
    """Test full favicon package generation orchestration."""
    # Test the full orchestration
    success = favicon_gen.generate_package(
        TEST_INPUT,
        TEST_OUTPUT_DIR,
        "Test Site",
        "Test",
        "#ff0000",
        "#ffffff",
        "/favicons",
    )
    assert success is True
    assert os.path.exists(os.path.join(TEST_OUTPUT_DIR, "favicon.ico"))
    assert os.path.exists(os.path.join(TEST_OUTPUT_DIR, "site.webmanifest"))
    assert os.path.exists(os.path.join(TEST_OUTPUT_DIR, "favicon-tags.html"))


def test_squish_protection():
    """Test image squish protection during resizing."""
    # Create a very wide image
    wide_input = "tests/wide_input.png"
    img = Image.new("RGBA", (1000, 500), (255, 0, 0, 255))
    img.save(wide_input)

    out_path = os.path.join(TEST_OUTPUT_DIR, "apple-touch-icon-wide.png")
    os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)

    # Generate apple touch icon (180x180)
    favicon_gen.generate_apple_touch_icon(wide_input, out_path)

    with Image.open(out_path) as out_img:
        assert out_img.size == (180, 180)
        # The red area should be 180x90, so at y=0 it should be
        # transparent (or bg color). By default bg is (0,0,0,0) in the function.
        assert out_img.getpixel((90, 10)) == (0, 0, 0, 0)  # Padding area
        assert out_img.getpixel((90, 90)) == (255, 0, 0, 255)  # Red area

    # Check ICO as well
    ico_path = os.path.join(TEST_OUTPUT_DIR, "favicon-wide.ico")
    favicon_gen.generate_favicon_ico(wide_input, ico_path)
    with Image.open(ico_path) as ico_img:
        # Check the 32x32 frame (Modern fallback size)
        assert ico_img.size == (32, 32)
        assert ico_img.getpixel((16, 4)) == (0, 0, 0, 0)  # Padding
        assert ico_img.getpixel((16, 16)) == (255, 0, 0, 255)  # Red

    os.remove(wide_input)
