# Photomosaic Generator

## Overview
This Streamlit app generates photomosaics by replacing regions of a main image with similar-colored tile images.

## Requirements
- Python 3.8+
- Streamlit
- OpenCV
- NumPy
- Pillow

## Installation
1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```
2. Upload a main image
3. Upload a ZIP file containing tile images
4. Adjust tile size using the slider
5. Generate and download your photomosaic!

## How It Works
- The app analyzes the average color of each region in the main image
- It finds the most color-similar tile image for each region
- Replaces the region with the selected tile image

## Customization
- Adjust tile size to control mosaic granularity
- Use different sets of tile images for unique effects
