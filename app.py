import streamlit as st
from PIL import Image
import numpy as np
import io
import base64

# Convert RGB to hex
def _from_rgb(rgb):
    return "#%02x%02x%02x" % rgb

# Get top N unique colors
def get_unique_colors(img, top_n=100):
    img = img.convert("RGB")
    img_array = np.array(img)
    reshaped = img_array.reshape(-1, 3)
    unique, counts = np.unique(reshaped, axis=0, return_counts=True)
    sorted_indices = np.argsort(-counts)
    top_colors = unique[sorted_indices][:top_n]
    return [tuple(c) for c in top_colors]

# Display color swatch with RGB and Hex
def display_color_block(color):
    hex_color = _from_rgb(color)
    rgb_text = f"RGB: {color}"
    hex_text = f"Hex: {hex_color}"

    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown(f"<div style='width:40px; height:40px; background:{hex_color}; border-radius:4px;'></div>", unsafe_allow_html=True)
    with col2:
        st.code(rgb_text)
        st.code(hex_text)

# Get pixel color from image
def get_color_at_point(image, x, y):
    if image.mode != "RGB":
        image = image.convert("RGB")
    return image.getpixel((x, y))

# Get average colors from grid blocks
def get_grid_average_colors(img, cols=6, rows=4):
    img = img.convert("RGB")
    img_array = np.array(img)
    h, w, _ = img_array.shape
    block_w = w // cols
    block_h = h // rows

    avg_colors = []
    for r in range(rows):
        row_colors = []
        for c in range(cols):
            x_start = c * block_w
            y_start = r * block_h
            block = img_array[y_start:y_start+block_h, x_start:x_start+block_w]
            avg_color = tuple(np.mean(block.reshape(-1, 3), axis=0).astype(int))
            row_colors.append(avg_color)
        avg_colors.append(row_colors)
    return avg_colors

# Streamlit App
def main():
    st.set_page_config(page_title="Image Color Picker", layout="wide")
    st.title("🎨 Image Color Picker Tool")

    uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        mode = st.radio("Select Mode", ["🎨 Color Palette", "🖱️ Color Picker", "🧩 Average Grid Palette"])

        if mode == "🎨 Color Palette":
            st.subheader("Top Colors in Image")
            top_n = st.slider("Number of Colors", 5, 100, 30)
            colors = get_unique_colors(image, top_n)

            for color in colors:
                display_color_block(color)

        elif mode == "🖱️ Color Picker":
            st.subheader("Select a Pixel Color by Grid Location")

            # Resize for display and coordinate mapping
            max_size = (400, 400)
            disp_img = image.copy()
            disp_img.thumbnail(max_size)
            disp_array = np.array(disp_img)

            h, w = disp_img.size
            st.image(disp_img, caption="Click Position Reference Image", width=w)

            st.markdown(f"Image Dimensions: **Width: {w}px**, **Height: {h}px**")
            
            # Grid-based coordinate selection
            st.subheader("Choose Pixel Coordinates")
            col1, col2 = st.columns(2)
            with col1:
                x = st.slider("X Coordinate", min_value=0, max_value=w - 1, step=1, value=w // 2)
            with col2:
                y = st.slider("Y Coordinate", min_value=0, max_value=h - 1, step=1, value=h // 2)

            try:
                color = get_color_at_point(disp_img, x, y)
                st.success(f"Selected Pixel Color at ({x}, {y})")
                display_color_block(color)
            except Exception as e:
                st.error("Invalid coordinates or image issue.")


        elif mode == "🧩 Average Grid Palette":
            st.subheader("Grid-based Average Colors")
            cols = st.slider("Grid Columns", 3, 12, 6)
            rows = st.slider("Grid Rows", 2, 10, 4)

            avg_colors_grid = get_grid_average_colors(image, cols, rows)

            for row_colors in avg_colors_grid:
                row_cols = st.columns(cols)
                for i, color in enumerate(row_colors):
                    with row_cols[i]:
                        display_color_block(color)

    else:
        st.info("Upload an image to begin.")

if __name__ == "__main__":
    main()
