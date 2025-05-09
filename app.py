import streamlit as st
import numpy as np
from PIL import Image
from streamlit_drawable_canvas import st_canvas

# --- Page Configuration ---
st.set_page_config(
    page_title="🎨 Simple Color Picker",
    layout="centered"
)

st.title("🎨 Color Picker Tool")
st.write("Upload an image and click anywhere to detect the color in **HEX** and **RGB** format.")

# --- HEX Converter ---
def rgb_to_hex(R, G, B):
    return '#{:02x}{:02x}{:02x}'.format(R, G, B).upper()

# --- Image Upload ---
uploaded_image = st.file_uploader("Upload an image (PNG/JPEG)", type=["png", "jpg", "jpeg"])

if uploaded_image:
    try:
        # Load and display image
        image = Image.open(uploaded_image).convert("RGB")
        image_np = np.array(image)
        st.image(image, caption="Click anywhere on the image to pick a color", use_column_width=True)

        # Canvas for picking color
        canvas_result = st_canvas(
            background_image=image,
            update_streamlit=True,
            height=image.height,
            width=image.width,
            drawing_mode="point",
            stroke_width=1,
            key="color_picker_canvas"
        )

        # Extract click position
        if canvas_result.json_data and canvas_result.json_data["objects"]:
            last_click = canvas_result.json_data["objects"][-1]
            x = int(last_click["left"])
            y = int(last_click["top"])
            R, G, B = image_np[y, x]
            hex_val = rgb_to_hex(R, G, B)

            st.markdown("### 🎯 Picked Color")
            st.color_picker("Color Preview", hex_val, disabled=True)
            st.code(f"HEX: {hex_val}")
            st.code(f"RGB: rgb({R}, {G}, {B})")

    except Exception as e:
        st.error(f"Something went wrong: {e}")
else:
    st.info("Please upload an image to begin.")
