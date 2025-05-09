import streamlit as st
import numpy as np
from PIL import Image
from streamlit_drawable_canvas import st_canvas

# --- Page Config ---
st.set_page_config(page_title="🎨 Image Color Picker", layout="centered")
st.title("🎯 Simple Image Color Picker")
st.caption("Upload an image and click on it to pick a color. Values are easy to copy.")

# --- Utility Functions ---
def rgb_to_hex(r, g, b):
    return '#{:02X}{:02X}{:02X}'.format(r, g, b)

def color_card(hex_val, rgb_str):
    """Display color swatch with copyable HEX and RGB."""
    st.markdown(f"""
    <div style="display: flex; align-items: center; margin-bottom: 1rem; border-radius: 12px;
                background: {hex_val}; padding: 1rem; color: {'#000' if sum(int(hex_val[i:i+2], 16) for i in (1,3,5)) > 382 else '#FFF'}">
        <div style="flex: 1;">
            <div style="font-weight: bold;">{hex_val}</div>
            <div>{rgb_str}</div>
        </div>
        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
            <button onclick="navigator.clipboard.writeText('{hex_val}')" style="cursor: pointer;">📋 Copy HEX</button>
            <button onclick="navigator.clipboard.writeText('{rgb_str}')" style="cursor: pointer;">📋 Copy RGB</button>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- Upload Image ---
uploaded_image = st.file_uploader("📷 Upload Image (PNG/JPG)", type=["png", "jpg", "jpeg"])

if uploaded_image:
    image = Image.open(uploaded_image).convert("RGB")
    image_np = np.array(image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # --- Canvas ---
    canvas_result = st_canvas(
        background_image=image,
        update_streamlit=True,
        height=image.height,
        width=image.width,
        drawing_mode="point",
        stroke_width=1,
        key="canvas_picker"
    )

    # --- Get Clicked Color ---
    if canvas_result.json_data and canvas_result.json_data["objects"]:
        click = canvas_result.json_data["objects"][-1]
        x, y = int(click["left"]), int(click["top"])

        if 0 <= y < image_np.shape[0] and 0 <= x < image_np.shape[1]:
            r, g, b = image_np[y, x]
            hex_val = rgb_to_hex(r, g, b)
            rgb_str = f"rgb({r}, {g}, {b})"

            st.markdown("### 🎨 Selected Color")
            color_card(hex_val, rgb_str)
        else:
            st.warning("⚠️ Clicked outside image bounds.")
else:
    st.info("Upload an image to begin.")
