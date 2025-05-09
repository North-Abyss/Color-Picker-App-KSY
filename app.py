import streamlit as st
from PIL import Image
import numpy as np
import matplotlib.colors as mcolors

# Function to convert RGB to Hex
def _from_rgb(rgb):
    return "#%02x%02x%02x" % rgb

# Function to get all unique colors from the image
def get_unique_colors(img):
    # Convert image to RGB and then numpy array
    img_rgb = img.convert('RGB')
    img_array = np.array(img_rgb)

    # Get unique colors and their frequency in the image
    unique_colors = {}
    for row in img_array:
        for pixel in row:
            color = tuple(pixel)
            if color not in unique_colors:
                unique_colors[color] = 1
            else:
                unique_colors[color] += 1
    return unique_colors

# Streamlit App
def main():
    st.title("Unique Colors from Image")

    # File upload for the image
    uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        # Load the image
        img = Image.open(uploaded_file)
        st.image(img, caption="Uploaded Image", use_column_width=True)

        # Get unique colors from the image
        unique_colors = get_unique_colors(img)

        # Display colors as squares with RGB and Hex values
        st.write("Unique Colors in the Image:")
        
        for color, count in unique_colors.items():
            hex_color = _from_rgb(color)
            
            # Create a square of the color
            col1, col2 = st.columns([1, 5])  # Create two columns
            with col1:
                st.markdown(f'<div style="background-color:{hex_color}; width: 30px; height: 30px;"></div>', unsafe_allow_html=True)
            with col2:
                st.write(f"RGB: {color}  Hex: {hex_color}")
                copy_rgb_button = st.button(f"Copy RGB {color}", key=f"copy_rgb_{color}")
                copy_hex_button = st.button(f"Copy Hex {hex_color}", key=f"copy_hex_{hex_color}")
                
                if copy_rgb_button:
                    st.text(f"Copied RGB: {color}")
                if copy_hex_button:
                    st.text(f"Copied Hex: {hex_color}")
                
    else:
        st.write("Please upload an image to see the unique colors.")

if __name__ == "__main__":
    main()
