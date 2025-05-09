import streamlit as st
from PIL import Image
import numpy as np
import io
import base64

# Convert RGB to hex
def _from_rgb(rgb):
    return "#%02x%02x%02x" % rgb

# Convert RGB to other formats (e.g., HSL, CMYK)
def rgb_to_hsl(rgb):
    r, g, b = rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    h = (mx + mn) / 2
    s = (mx - mn) / 2 if mx == mn else (mx - mn) / (1 - abs(2 * h - 1))
    l = (mx + mn) / 2
    return tuple(int(c * 255) for c in (h, s, l))

def rgb_to_cmyk(rgb):
    r, g, b = rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0
    k = 1 - max(r, g, b)
    c = (1 - r - k) / (1 - k)
    m = (1 - g - k) / (1 - k)
    y = (1 - b - k) / (1 - k)
    return tuple([int(val * 100) for val in (c, m, y, k)])

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
def display_color_block(color, format_type="RGB"):
    hex_color = _from_rgb(color)
    rgb_text = f"RGB: {color}"
    hex_text = f"Hex: {hex_color}"

    if format_type == "HSL":
        hsl = rgb_to_hsl(color)
        hsl_text = f"HSL: {hsl}"
        display_text = hsl_text
    elif format_type == "CMYK":
        cmyk = rgb_to_cmyk(color)
        cmyk_text = f"CMYK: {cmyk}"
        display_text = cmyk_text
    else:
        display_text = rgb_text
    
    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown(
            f"<div style='width:40px; height:40px; background:{hex_color}; border-radius:4px;'></div>",
            unsafe_allow_html=True
        )
    with col2:
        st.code(display_text)
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
            block = img_array[y_start:y_start + block_h, x_start:x_start + block_w]
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

        mode = st.radio("Select Mode",
                        ["🎨 Color Palette", "🖱️ Color Picker", "🧩 Average Grid Palette"],
                        index=1  # This sets "🖱️ Color Picker" as default 
                       )

        if mode == "🎨 Color Palette":
            st.subheader("Top Colors in Image")
            top_n = st.slider("Number of Colors", 5, 100, 30)
            colors = get_unique_colors(image, top_n)

            for color in colors:
                display_color_block(color)

        elif mode == "🖱️ Color Picker":
            st.subheader("🎯 Pixel Color Selector")

            max_size = (400, 400)
            disp_img = image.copy()
            disp_img.thumbnail(max_size)
            width, height = disp_img.size

            # Initial coordinate values
            if 'x' not in st.session_state:
                st.session_state.x = width // 2
            if 'y' not in st.session_state:
                st.session_state.y = height // 2

            # Display the current coordinates
            st.write(f"Current Coordinates: X = {st.session_state.x}, Y = {st.session_state.y}")

            # Sliders for fine adjustment (X and Y)
            col1, col2 = st.columns(2)
            with col1:
                st.session_state.x = st.slider("Select X Coordinate", 0, width - 1, st.session_state.x)
            with col2:
                st.session_state.y = st.slider("Select Y Coordinate", 0, height - 1, st.session_state.y)

            # Buttons for fine adjustment (increasing/decreasing X and Y by 1)
            col3, col4 = st.columns(2)
            with col3:
                if st.button('X+'):
                    st.session_state.x = min(st.session_state.x + 1, width - 1)
            with col4:
                if st.button('X-'):
                    st.session_state.x = max(st.session_state.x - 1, 0)

            col5, col6 = st.columns(2)
            with col5:
                if st.button('Y+'):
                    st.session_state.y = min(st.session_state.y + 1, height - 1)
            with col6:
                if st.button('Y-'):
                    st.session_state.y = max(st.session_state.y - 1, 0)

            # Convert image to base64
            buffered = io.BytesIO()
            disp_img.save(buffered, format="PNG")
            img_b64 = base64.b64encode(buffered.getvalue()).decode()

            # Display image with crosshair
            st.markdown(f"""
            <div style="position: relative; display: inline-block; border: 1px solid #ccc;">
                <img src="data:image/png;base64,{img_b64}" width="{width}" height="{height}">
                <div style="position: absolute; top: 0; left: {st.session_state.x}px; width: 1px; height: {height}px; background-color: red;"></div>
                <div style="position: absolute; top: {st.session_state.y}px; left: 0; width: {width}px; height: 1px; background-color: red;"></div>
            </div>
            """, unsafe_allow_html=True)

            try:
                color = get_color_at_point(disp_img, st.session_state.x, st.session_state.y)
                st.success(f"Selected Pixel Color at ({st.session_state.x}, {st.session_state.y})")
                st.write(f"RGB: {color}")
            except Exception:
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
