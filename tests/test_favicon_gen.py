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
    color = favicon_gen.extract_dominant_color(TEST_INPUT)
    assert color.startswith("#")
    assert len(color) == 7
    # Since we created a red image, it should detect red
    assert color.lower() == "#ff0000"

def test_validate_input_file():
    assert favicon_gen.validate_input_file(TEST_INPUT) is True
    assert favicon_gen.validate_input_file("non_existent.png") is False

def test_validate_color_hex():
    assert favicon_gen.validate_color_hex("#ffffff") is True
    assert favicon_gen.validate_color_hex("white") is False
    assert favicon_gen.validate_color_hex("#fff") is False # It expects 6 chars

def test_generate_favicon_ico():
    out_path = os.path.join(TEST_OUTPUT_DIR, "favicon.ico")
    os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)
    assert favicon_gen.generate_favicon_ico(TEST_INPUT, out_path) is True
    assert os.path.exists(out_path)

def test_generate_apple_touch_icon():
    out_path = os.path.join(TEST_OUTPUT_DIR, "apple-touch-icon.png")
    os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)
    assert favicon_gen.generate_apple_touch_icon(TEST_INPUT, out_path) is True
    assert os.path.exists(out_path)
    with Image.open(out_path) as img:
        assert img.size == (180, 180)

def test_generate_site_webmanifest():
    out_path = os.path.join(TEST_OUTPUT_DIR, "site.webmanifest")
    os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)
    assert favicon_gen.generate_site_webmanifest(out_path) is True
    assert os.path.exists(out_path)

def test_generate_package():
    # Test the full orchestration
    success = favicon_gen.generate_package(
        TEST_INPUT, TEST_OUTPUT_DIR, "Test Site", "Test", 
        "#ff0000", "#ffffff", "/favicons"
    )
    assert success is True
    assert os.path.exists(os.path.join(TEST_OUTPUT_DIR, "favicon.ico"))
    assert os.path.exists(os.path.join(TEST_OUTPUT_DIR, "site.webmanifest"))
    assert os.path.exists(os.path.join(TEST_OUTPUT_DIR, "favicon-tags.html"))
