import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import colorsys
import re

# --- Load color data ---
@st.cache_data
def load_colors():
    url = "https://raw.githubusercontent.com/codebrainz/color-names/master/output/colors.csv"
    return pd.read_csv(url)

colors_df = load_colors()

# --- Color conversions ---
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

# --- Streamlit Page Config ---
st.set_page_config(
    page_title="🎨 Color Detector",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown(
    """
    <style>
        body {
            background-color: #f5f7fa;
        }
        .stApp {
            background-color: #f0f4f8;
        }
        h1, h2, h3 {
            color: #2c3e50;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- App UI ---
st.title("🎨 Color Detector App")
st.write("Upload an image and click anywhere to detect color name and values in **HEX**, **RGB**, **HSL**, **CMYK** formats.")
st.write("Alternatively, you can **paste a color code** (HEX, RGB, HSL, CMYK) to quickly get the matching color.")

# --- Color Input Section ---
color_input = st.text_input("🔎 Paste a color code (HEX, RGB, HSL, CMYK)")

if color_input:
    # Handle HEX input
    hex_match = re.match(r'^#?([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$', color_input)
    if hex_match:
        hex_val = hex_match.group(0)
        R, G, B = [int(hex_val[i:i+2], 16) for i in (1, 3, 5)]
        hsl_val = rgb_to_hsl(R, G, B)
        cmyk_val = rgb_to_cmyk(R, G, B)
        color_name = get_closest_color_name(R, G, B)

        st.markdown(f"### 🎯 Detected Color (from input): {color_name}")
        st.color_picker("Preview", hex_val, disabled=True)
        st.write(f"**HEX:** `{hex_val.upper()}`")
        st.write(f"**RGB:** `rgb({R}, {G}, {B})`")
        st.write(f"**HSL:** `{hsl_val}`")
        st.write(f"**CMYK:** `{cmyk_val}`")

    # Handle RGB input (e.g., rgb(255, 0, 0))
    elif re.match(r'^rgb\(\d{1,3}, \d{1,3}, \d{1,3}\)$', color_input.strip()):
        rgb_match = re.match(r'rgb\((\d+), (\d+), (\d+)\)', color_input.strip())
        R, G, B = int(rgb_match.group(1)), int(rgb_match.group(2)), int(rgb_match.group(3))
        hex_val = rgb_to_hex(R, G, B)
        hsl_val = rgb_to_hsl(R, G, B)
        cmyk_val = rgb_to_cmyk(R, G, B)
        color_name = get_closest_color_name(R, G, B)

        st.markdown(f"### 🎯 Detected Color (from input): {color_name}")
        st.color_picker("Preview", hex_val, disabled=True)
        st.write(f"**RGB:** `rgb({R}, {G}, {B})`")
        st.write(f"**HEX:** `{hex_val.upper()}`")
        st.write(f"**HSL:** `{hsl_val}`")
        st.write(f"**CMYK:** `{cmyk_val}`")

    # Handle HSL input (e.g., hsl(360, 100%, 100%))
    elif re.match(r'^hsl\(\d{1,3}, \d{1,3}%, \d{1,3}%\)$', color_input.strip()):
        hsl_match = re.match(r'hsl\((\d+), (\d+)%?, (\d+)%?\)', color_input.strip())
        h, s, l = int(hsl_match.group(1)), int(hsl_match.group(2)), int(hsl_match.group(3))
        R, G, B = colorsys.hls_to_rgb(h / 360, l / 100, s / 100)
        R, G, B = [int(c * 255) for c in (R, G, B)]
        hex_val = rgb_to_hex(R, G, B)
        cmyk_val = rgb_to_cmyk(R, G, B)
        color_name = get_closest_color_name(R, G, B)

        st.markdown(f"### 🎯 Detected Color (from input): {color_name}")
        st.color_picker("Preview", hex_val, disabled=True)
        st.write(f"**HSL:** `{color_input.strip()}`")
        st.write(f"**RGB:** `rgb({R}, {G}, {B})`")
        st.write(f"**HEX:** `{hex_val.upper()}`")
        st.write(f"**CMYK:** `{cmyk_val}`")

    # Handle CMYK input (e.g., cmyk(0%, 100%, 100%, 0%))
    elif re.match(r'^cmyk\(\d{1,3}%, \d{1,3}%, \d{1,3}%, \d{1,3}%\)$', color_input.strip()):
        cmyk_match = re.match(r'cmyk\((\d+)%?, (\d+)%?, (\d+)%?, (\d+)%?\)', color_input.strip())
        C, M, Y, K = int(cmyk_match.group(1)), int(cmyk_match.group(2)), int(cmyk_match.group(3)), int(cmyk_match.group(4))
        R = 255 * (1 - C / 100) * (1 - K / 100)
        G = 255 * (1 - M / 100) * (1 - K / 100)
        B = 255 * (1 - Y / 100) * (1 - K / 100)
        R, G, B = [int(c) for c in (R, G, B)]
        hex_val = rgb_to_hex(R, G, B)
        hsl_val = rgb_to_hsl(R, G, B)
        color_name = get_closest_color_name(R, G, B)

        st.markdown(f"### 🎯 Detected Color (from input): {color_name}")
        st.color_picker("Preview", hex_val, disabled=True)
        st.write(f"**CMYK:** `{color_input.strip()}`")
        st.write(f"**RGB:** `rgb({R}, {G}, {B})`")
        st.write(f"**HEX:** `{hex_val.upper()}`")
        st.write(f"**HSL:** `{hsl_val}`")

# --- Image Upload Section ---
uploaded_file = st.file_uploader("📤 Or, upload an image to pick a color", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert('RGB')
    image_np = np.array(image)
    st.image(image, caption="🖱️ Click on the image below to pick a color", use_column_width=True)

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
        st.write(f"**Name:** `{color_name}`")
        st.write(f"**HEX:** `{hex_val.upper()}`")
        st.write(f"**RGB:** `rgb({R}, {G}, {B})`")
        st.write(f"**HSL:** `{hsl_val}`")
        st.write(f"**CMYK:** `{cmyk_val}`")
