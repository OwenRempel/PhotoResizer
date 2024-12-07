# Image Resizer

This Python script allows you to batch resize images in a specified input folder and save them in an output folder, resizing each image to various predefined dimensions. It supports multiple image formats such as PNG, JPG, and JPEG. The script utilizes multithreading to process images concurrently, improving performance for large image sets.

## Features

- Resize images to multiple sizes while maintaining aspect ratio.
- Process images concurrently using threading for faster performance.
- Supports common image formats (PNG, JPG, JPEG).
- Saves resized images in the same directory structure as the original files.

## Requirements

- Python 3.x
- Pillow, `PIL` library
- Threading (standard Python library)

### Install Dependencies

You can install the required dependencies using pip:

```bash
pip install pillow
