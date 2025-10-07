# Image Watermarking Tool

A Python automation tool that downloads product images from a cannabis dispensary website and applies watermarks, or watermarks local images in bulk.

## Features

- **Web Scraping Mode**: Automatically navigates to an online menu, scrolls to load all products, downloads product images, and applies watermarks
- **Local Mode**: Batch watermarks images from a local folder
- Headless Chrome automation using Selenium
- Transparent watermark overlay with customizable opacity
- Automatic watermark sizing relative to base image dimensions

## Requirements

### Python Packages
```bash
pip install selenium pillow requests
```

Or, alternatively:

```bash
pip install requirements.txt
```

### Additional Requirements
- **ChromeDriver**: Must be installed and accessible in your PATH
- **Chrome Browser**: Required for Selenium WebDriver
- **badge.png**: Watermark image file (must be present in the root directory)

## Project Structure

```
project/
├── run.py              # Main script
├── badge.png           # Your watermark image
├── unmarked-images/    # Input folder for images
└── complete-images/    # Output folder for watermarked images
```

**Note**: Create the `unmarked-images/` and `complete-images/` directories before running the script.

## Usage

Run the script:
```bash
python run.py
```

You'll be prompted to choose a mode:

### Web Mode
- Enter `web` when prompted
- The script will:
  - Navigate to the online menu
  - Handle age verification automatically
  - Scroll through the entire product catalog
  - Download all product images to `unmarked-images/`
  - Apply watermarks and save to `complete-images/`

### Local Mode
- Enter `local` when prompted
- Place your images in the `unmarked-images/` folder
- Press Enter to process all images
- Watermarked images will be saved to `complete-images/`

## Watermark Configuration

The watermark is applied with the following settings:
- **Size**: 25% of the base image width (maintaining aspect ratio)
- **Opacity**: 75% transparency
- **Position**: Top-right corner with 50px padding from edges

To modify these settings, edit the `apply_watermark()` function:
```python
wm_width = base_image.width // 4  # Change divisor to adjust size
alpha = alpha.point(lambda i: i * 0.75)  # Change 0.75 for different opacity
pos_x = base_image.width - watermark.width - 50  # Adjust position
pos_y = 50  # Adjust vertical position
```

## Technical Details

### Selenium Configuration
The script uses headless Chrome with optimized options:
- `--headless=new`: Modern headless mode
- `--disable-gpu`: Better compatibility on Windows
- `--no-sandbox`: Required for Linux/container environments
- `--log-level=3`: Suppresses verbose logging

### Image Processing
- Uses PIL (Pillow) for image manipulation
- Supports PNG and JPEG formats
- Preserves image quality while converting to RGB for final output
- Uses LANCZOS resampling for high-quality watermark resizing

## Limitations

- Hardcoded URL specific to one dispensary website
- Requires the exact HTML structure of the target website
- Age verification bypass is site-specific

## Troubleshooting

**ChromeDriver errors**: Ensure ChromeDriver version matches your Chrome browser version

**Image not found**: Verify `badge.png` exists in the root directory

**Folder errors**: Create `unmarked-images/` and `complete-images/` directories before running

**Selenium timeouts**: Increase `time.sleep()` values if the website loads slowly

## License

This tool is provided as-is for educational purposes.