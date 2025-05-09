import streamlit as st
import numpy as np
from PIL import Image
from streamlit_drawable_canvas import st_canvas

# Page config
st.set_page_config(page_title="🎨 Image Color Picker", layout="centered")
st.title("🎯 Simple Image Color Picker")
st.caption("Upload an image and click anywhere to detect a color. Easily copy RGB or HEX.")

# Convert RGB to HEX
def rgb_to_hex(r, g, b):
    return '#{:02X}{:02X}{:02X}'.format(r, g, b)

# Image uploader
uploaded_image = st.file_uploader("📷 Upload Image (PNG/JPG)", type=["png", "jpg", "jpeg"])

if uploaded_image:
    image = Image.open(uploaded_image).convert("RGB")
    image_np = np.array(image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Canvas to click on image
    canvas_result = st_canvas(
        background_image=image,
        update_streamlit=True,
        height=image.height,
        width=image.width,
        drawing_mode="point",
        stroke_width=1,
        key="canvas_picker"
    )

    # If a point was clicked
    if canvas_result.json_data and canvas_result.json_data["objects"]:
        click = canvas_result.json_data["objects"][-1]
        x = int(click["left"])
        y = int(click["top"])
        r, g, b = image_np[y, x]
        hex_val = rgb_to_hex(r, g, b)

        st.markdown("### 🎨 Picked Color")
        st.color_picker("Color Preview", hex_val, disabled=True)

        col1, col2 = st.columns(2)
        with col1:
            st.code(f"{hex_val}", language="bash")
            st.button("📋 Copy HEX", on_click=lambda: st.toast("HEX copied!"))
        with col2:
            st.code(f"rgb({r}, {g}, {b})", language="bash")
            st.button("📋 Copy RGB", on_click=lambda: st.toast("RGB copied!"))

else:
    st.info("Upload an image to get started.")
