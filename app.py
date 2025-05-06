import streamlit as st
import numpy as np
import pandas as pd
import cv2
from PIL import Image
from io import BytesIO
import colorsys

@st.cache_data
def load_colors():
    url = "https://raw.githubusercontent.com/codebrainz/color-names/master/output/colors.csv"
    return pd.read_csv(url)

colors_df = load_colors()

def get_closest_color_name(R, G, B):
    min_dist = float("inf")
    closest_name = ""
    for _, row in colors_df.iterrows():
        d = np.sqrt((R - row['r'])**2 + (G - row['g'])**2 + (B - row['b'])**2)
        if d < min_dist:
            min_dist = d
            closest_name = row['name']
    return closest_name

def rgb_to_hex(R, G, B):
    return '#%02x%02x%02x' % (R, G, B)

def rgb_to_hsl(R, G, B):
    h, l, s = colorsys.rgb_to_hls(R/255, G/255, B/255)
    return f"hsl({int(h*360)}, {int(s*100)}%, {int(l*100)}%)"

def rgb_to_cmyk(R, G, B):
    if (R, G, B) == (0, 0, 0):
        return "cmyk(0%, 0%, 0%, 100%)"
    C = 1 - R / 255
    M = 1 - G / 255
    Y = 1 - B / 255
    K = min(C, M, Y)
    C = (C - K) / (1 - K)
    M = (M - K) / (1 - K)
    Y = (Y - K) / (1 - K)
    return f"cmyk({int(C*100)}%, {int(M*100)}%, {int(Y*100)}%, {int(K*100)}%)"

st.set_page_config(page_title="Color Detector", layout="centered")
st.title("🎨 Color Detector App")
st.write("Upload an image and click to detect color name + values in HEX, RGB, HSL, CMYK.")

uploaded_file = st.file_uploader("Upload an image (PNG, JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert('RGB')
    image_np = np.array(image)
    st.image(image, caption="Click on the image below to pick a color")

    from streamlit_drawable_canvas import st_canvas
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=1,
        background_image=image,
        update_streamlit=True,
        height=image.height,
        width=image.width,
        drawing_mode="point",
        key="canvas",
    )

    if canvas_result.json_data and canvas_result.json_data["objects"]:
        x = int(canvas_result.json_data["objects"][-1]["left"])
        y = int(canvas_result.json_data["objects"][-1]["top"])
        R, G, B = image_np[y, x]
        hex_val = rgb_to_hex(R, G, B)
        hsl_val = rgb_to_hsl(R, G, B)
        cmyk_val = rgb_to_cmyk(R, G, B)
        color_name = get_closest_color_name(R, G, B)

        st.markdown("---")
        st.markdown(f"### 🎯 Detected Color at ({x}, {y})")
        st.color_picker("Preview", hex_val, disabled=True)
        st.write(f"**Name:** {color_name}")
        st.write(f"**RGB:** ({R}, {G}, {B})")
        st.write(f"**HEX:** `{hex_val.upper()}`")
        st.write(f"**HSL:** `{hsl_val}`")
        st.write(f"**CMYK:** `{cmyk_val}`")
