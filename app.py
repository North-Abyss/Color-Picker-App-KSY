def main():
    st.set_page_config(page_title="Image Color Picker", layout="wide")
    st.title("🎨 Image Color Picker Tool")

    # Upload image
    uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, use_column_width=True)

        # Mode toggle
        mode = st.radio("Select Mode", ["🎨 Color Palette", "🖱️ Color Picker", "🧩 Average Grid Palette"])

        if mode == "🎨 Color Palette":
            st.subheader("Top Colors in Image")
            top_n = st.slider("Number of Colors", 5, 100, 30)
            colors = get_unique_colors(image, top_n)

            for color in colors:
                display_color_block(color)

        elif mode == "🖱️ Color Picker":
            st.subheader("Click on the image to pick a color")

            max_size = (500, 500)
            disp_img = image.copy()
            disp_img.thumbnail(max_size)

            x = st.number_input("X coordinate", min_value=0, max_value=disp_img.width - 1, value=0)
            y = st.number_input("Y coordinate", min_value=0, max_value=disp_img.height - 1, value=0)

            try:
                color = get_color_at_point(disp_img, x, y)
                st.success("Selected Color")
                display_color_block(color)
            except:
                st.error("Invalid coordinates")

        elif mode == "🧩 Average Grid Palette":
            st.subheader("Grid-based Average Colors")

            # Choose grid size
            cols = st.slider("Number of Columns", 3, 12, 6)
            rows = st.slider("Number of Rows", 2, 10, 4)

            img = image.convert("RGB")
            img_array = np.array(img)
            h, w, _ = img_array.shape

            block_w = w // cols
            block_h = h // rows

            for r in range(rows):
                st.markdown("---")
                cols_in_row = st.columns(cols)
                for c in range(cols):
                    x_start = c * block_w
                    y_start = r * block_h
                    block = img_array[y_start:y_start + block_h, x_start:x_start + block_w]
                    avg_color = tuple(np.mean(block.reshape(-1, 3), axis=0).astype(int))
                    with cols_in_row[c]:
                        display_color_block(avg_color)

    else:
        st.info("Upload an image to begin.")
