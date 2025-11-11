---
name: screenshot-processor
description: Process, analyze, and annotate screenshots and images. Use when working with screenshots, image analysis, OCR text extraction, image comparison, or creating annotated documentation. Supports batch processing and automation.
---

# Screenshot Processor

Advanced screenshot and image processing for documentation, analysis, and automation.

## Core Capabilities

1. **Image Analysis**: Extract information and analyze screenshots
2. **OCR Text Extraction**: Extract text from images
3. **Image Comparison**: Detect differences between screenshots
4. **Batch Processing**: Process multiple screenshots automatically
5. **Organization**: Sort and categorize screenshots
6. **Metadata Management**: Extract and manage image metadata

## Instructions

### Screenshot Analysis Workflow

1. **Inspect Screenshot**
   - Read the image file
   - Extract dimensions and format
   - Identify content type
   - Check image quality

2. **Process Content**
   - Extract text using OCR if needed
   - Identify UI elements
   - Detect patterns or anomalies
   - Extract relevant information

3. **Document Findings**
   - Describe what's in the screenshot
   - Extract important text
   - Note any issues or observations
   - Provide context

4. **Organize**
   - Rename with descriptive names
   - Move to appropriate folders
   - Update metadata
   - Create index or catalog

## Common Tasks

### Extract Text from Screenshots

```bash
# Using tesseract for OCR
tesseract screenshot.png output.txt

# With specific language
tesseract screenshot.png output -l eng

# Get confidence scores
tesseract screenshot.png output.txt --oem 3 -c debug_file=/dev/null
```

### Image Information

```bash
# Get image details with ImageMagick
identify -verbose screenshot.png

# Basic info
file screenshot.png

# Image dimensions
identify -format "%wx%h" screenshot.png
```

### Batch Processing

```bash
# Convert all PNG to JPG
for file in *.png; do
    convert "$file" "${file%.png}.jpg"
done

# Resize all screenshots
for file in *.png; do
    convert "$file" -resize 1920x1080 "resized_$file"
done

# Extract text from all screenshots
for file in *.png; do
    tesseract "$file" "${file%.png}_text.txt"
done
```

### Image Comparison

```bash
# Compare two images with ImageMagick
compare -metric RMSE image1.png image2.png diff.png

# Visual diff
compare image1.png image2.png -compose src diff.png
```

## Python Image Processing

### Using Pillow (PIL)

```python
from PIL import Image, ImageDraw, ImageFont
import os

# Load and analyze image
img = Image.open('screenshot.png')
print(f"Size: {img.size}")
print(f"Format: {img.format}")
print(f"Mode: {img.mode}")

# Resize image
img_resized = img.resize((800, 600))
img_resized.save('screenshot_small.png')

# Crop image
box = (100, 100, 400, 400)
img_cropped = img.crop(box)
img_cropped.save('screenshot_cropped.png')

# Add annotation
draw = ImageDraw.Draw(img)
font = ImageFont.load_default()
draw.text((10, 10), "Annotation", fill='red', font=font)
img.save('screenshot_annotated.png')
```

### Using OpenCV

```python
import cv2
import numpy as np

# Load image
img = cv2.imread('screenshot.png')

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect edges
edges = cv2.Canny(gray, 100, 200)

# Find contours
contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Save result
cv2.imwrite('screenshot_edges.png', edges)
```

### OCR with pytesseract

```python
from PIL import Image
import pytesseract

# Extract text
img = Image.open('screenshot.png')
text = pytesseract.image_to_string(img)
print(text)

# Get detailed data
data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
print(data['text'])

# Get bounding boxes
boxes = pytesseract.image_to_boxes(img)
print(boxes)
```

## Screenshot Organization

### Naming Conventions

```bash
# Format: YYYY-MM-DD_HH-MM-SS_description.png
screenshot_2025-11-11_14-30-45_login-page.png
screenshot_2025-11-11_14-31-12_dashboard.png
screenshot_2025-11-11_14-32-03_error-message.png
```

### Categorization

```
screenshots/
├── ui/
│   ├── login/
│   ├── dashboard/
│   └── settings/
├── errors/
│   ├── critical/
│   └── warnings/
├── documentation/
│   ├── setup/
│   └── usage/
└── testing/
    ├── before/
    └── after/
```

## Metadata Management

### Extract EXIF Data

```python
from PIL import Image
from PIL.ExifTags import TAGS

img = Image.open('screenshot.png')
exif_data = img._getexif()

if exif_data:
    for tag_id, value in exif_data.items():
        tag = TAGS.get(tag_id, tag_id)
        print(f"{tag}: {value}")
```

### Add Custom Metadata

```python
from PIL import Image
from PIL.PngImagePlugin import PngInfo

# Create metadata
metadata = PngInfo()
metadata.add_text("Author", "Claude Code")
metadata.add_text("Description", "Login page screenshot")
metadata.add_text("Date", "2025-11-11")
metadata.add_text("Project", "Desktop System")

# Save with metadata
img = Image.open('screenshot.png')
img.save('screenshot_with_metadata.png', pnginfo=metadata)

# Read metadata
img = Image.open('screenshot_with_metadata.png')
print(img.info)
```

## Automation Scripts

### Screenshot Organizer

```python
import os
import shutil
from datetime import datetime
from PIL import Image
import pytesseract

def organize_screenshots(source_dir, dest_dir):
    """Organize screenshots by date and content"""

    for filename in os.listdir(source_dir):
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        filepath = os.path.join(source_dir, filename)
        img = Image.open(filepath)

        # Get creation date
        stat = os.stat(filepath)
        date = datetime.fromtimestamp(stat.st_mtime)
        date_dir = date.strftime('%Y-%m-%d')

        # Extract text to determine category
        text = pytesseract.image_to_string(img).lower()

        # Categorize
        if 'error' in text:
            category = 'errors'
        elif 'login' in text or 'password' in text:
            category = 'authentication'
        elif 'dashboard' in text:
            category = 'dashboard'
        else:
            category = 'general'

        # Create destination directory
        dest_path = os.path.join(dest_dir, category, date_dir)
        os.makedirs(dest_path, exist_ok=True)

        # Move file
        shutil.move(filepath, os.path.join(dest_path, filename))
        print(f"Moved {filename} to {category}/{date_dir}")

# Usage
organize_screenshots('~/Desktop/screenshots', '~/Documents/organized_screenshots')
```

## Best Practices

1. **Naming**: Use descriptive, dated filenames
2. **Quality**: Capture at appropriate resolution
3. **Privacy**: Redact sensitive information
4. **Storage**: Organize systematically
5. **Documentation**: Add context and descriptions

## Common Use Cases

- **Bug Reporting**: Capture and annotate error screenshots
- **Documentation**: Create visual guides and tutorials
- **Testing**: Compare UI changes before/after
- **Analysis**: Extract data from visual reports
- **Archival**: Organize historical screenshots

## Integration with Other Skills

- Use with **document-generator** to create visual documentation
- Combine with **desktop-file-organizer** for screenshot management
- Work with **local-data-analyzer** to analyze extracted text data
