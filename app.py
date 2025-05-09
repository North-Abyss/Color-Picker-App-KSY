import streamlit as st
from PIL import Image
import io

# Function to convert RGB to Hex
def _from_rgb(rgb):
    return "#%02x%02x%02x" % rgb

# Function to get color from a clicked pixel
def get_color_from_image(img, x, y):
    pixel = img.getpixel((x, y))
    hex_color = _from_rgb(pixel)
    return pixel, hex_color

# Streamlit App
def main():
    st.title("Click on the Image to Pick a Color")

    # File upload for the image
    uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        # Load the image
        img = Image.open(uploaded_file)
        st.image(img, caption="Uploaded Image", use_column_width=True)

        # Convert the image to a format for processing
        img = img.convert("RGB")

        # Let the user click on the image and get pixel color
        st.write("Click on the image to pick a color (not implemented directly in Streamlit).")

        # Placeholder for displaying the color values
        color_container = st.empty()
        color_container.text("Color values will be shown here.")

        # Add button to open another image
        if st.button("Open Another Image"):
            main()

        # Handle the color extraction via mouse click (using an external tool like OpenCV, as Streamlit doesn't handle mouse events natively)
        # Since Streamlit can't capture mouse events over images, you'd need to handle this differently, e.g., through manual input
        st.warning("Mouse click event is not directly supported in Streamlit, consider alternative ways to select color.")

if __name__ == "__main__":
    main()
