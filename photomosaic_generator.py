import os
import cv2
import numpy as np
import streamlit as st
from PIL import Image

class PhotomosaicGenerator:
    def __init__(self, tile_size=20):
        self.tile_size = tile_size

    def _get_average_color(self, image):
        """Calculate the average color of an image."""
        return np.mean(image, axis=(0, 1)).astype(int)

    def _find_best_match(self, target_color, tile_colors):
        """Find the tile with the closest average color."""
        return np.argmin(np.sum((tile_colors - target_color) ** 2, axis=1))

    def generate_photomosaic(self, main_image, tile_images):
        """Generate photomosaic from main image and tile images."""
        # Resize main image to be divisible by tile size
        h, w = main_image.shape[:2]
        h = h - (h % self.tile_size)
        w = w - (w % self.tile_size)
        main_image = main_image[:h, :w]

        # Preprocess tile images
        resized_tiles = []
        tile_colors = []
        for tile in tile_images:
            resized_tile = cv2.resize(tile, (self.tile_size, self.tile_size))
            resized_tiles.append(resized_tile)
            tile_colors.append(self._get_average_color(resized_tile))
        tile_colors = np.array(tile_colors)

        # Create mosaic
        mosaic = np.zeros_like(main_image)
        for y in range(0, h, self.tile_size):
            for x in range(0, w, self.tile_size):
                tile_region = main_image[y:y+self.tile_size, x:x+self.tile_size]
                avg_color = self._get_average_color(tile_region)
                best_match_idx = self._find_best_match(avg_color, tile_colors)
                mosaic[y:y+self.tile_size, x:x+self.tile_size] = resized_tiles[best_match_idx]

        return mosaic

def load_tile_images(directory):
    """Load tile images from a directory."""
    tile_images = []
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            filepath = os.path.join(directory, filename)
            img = cv2.imread(filepath)
            if img is not None:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                tile_images.append(img)
    return tile_images
