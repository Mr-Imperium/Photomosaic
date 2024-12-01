import os
import cv2
import numpy as np
import streamlit as st
from PIL import Image

# Import the PhotomosaicGenerator from the previous script
from photomosaic_generator import PhotomosaicGenerator, load_tile_images

def main():
    st.title("📸 Photomosaic Generator")
    
    # Sidebar for configuration
    st.sidebar.header("Configuration")
    tile_size = st.sidebar.slider("Tile Size", min_value=10, max_value=50, value=20)
    
    # Main image upload
    st.sidebar.header("Upload Images")
    main_image = st.sidebar.file_uploader("Choose Main Image", type=['png', 'jpg', 'jpeg'])
    tile_directory = st.sidebar.file_uploader("Upload Tile Images Directory", type=['zip'])
    
    if main_image and tile_directory:
        # Process main image
        main_image = Image.open(main_image)
        main_image_cv = cv2.cvtColor(np.array(main_image), cv2.COLOR_RGB2BGR)
        
        # Extract and process tile images
        import tempfile
        import zipfile
        
        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(tile_directory, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            tile_images = load_tile_images(temp_dir)
        
        if tile_images:
            # Generate photomosaic
            generator = PhotomosaicGenerator(tile_size=tile_size)
            mosaic = generator.generate_photomosaic(main_image_cv, tile_images)
            
            # Display results
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Original Image")
                st.image(main_image)
            
            with col2:
                st.subheader("Photomosaic")
                st.image(mosaic)
            
            # Download option
            st.download_button(
                label="Download Photomosaic",
                data=cv2.imencode('.png', cv2.cvtColor(mosaic, cv2.COLOR_RGB2BGR))[1].tobytes(),
                file_name='photomosaic.png',
                mime='image/png'
            )
        else:
            st.error("No valid tile images found in the uploaded directory.")

if __name__ == "__main__":
    main()
