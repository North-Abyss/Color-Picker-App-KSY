
# 🎨 Color Picker App KSY

A real-time, pixel-accurate color detection tool for designers, developers, artists, and creators. Upload or drag-and-drop any image, click anywhere on it, and instantly view the closest **color name**, along with its **HEX**, **RGB**, **HSL**, and **CMYK** values — all in one sleek, interactive interface.

🌐 **Live Demo** → [Try on Streamlit Cloud](https://color-picker-app-ksy.streamlit.app/)

---

## 🚀 Features

✅ **Upload or Drag-and-Drop** images  
✅ **Click anywhere** on the image to pick a color  
✅ Get the closest **named color** from an open-source dataset  
✅ Instant color preview with values in:
- 🎨 HEX (e.g. `#FFA500`)
- 🔵 RGB (e.g. `rgb(255,165,0)`)
- 🎚 HSL (e.g. `hsl(39,100%,50%)`)
- 🖨 CMYK (e.g. `cmyk(0%, 35%, 100%, 0%)`)

✅ Fully web-based via **Streamlit Cloud**  
✅ Clean, responsive UI  
✅ Dataset auto-loaded from GitHub — always up to date  
✅ Built for speed, accuracy, and simplicity

---

## 🖼️ How It Works

1. Upload or drag-and-drop an image (JPG, PNG)
2. Click on any pixel using the canvas
3. The app fetches:
   - Pixel color value
   - Closest named color from the dataset
   - HEX, RGB, HSL, and CMYK representations
4. The selected color is previewed alongside all format values

---

## 📸 Demo

![Demo Screenshot](https://raw.githubusercontent.com/North-Abyss/Color-Picker-App-KSY/main/Color%20Picker%20Demo%20Streamlit.png)

---

## 🧠 Tech Stack

| Tech | Purpose |
|------|---------|
| [Streamlit](https://streamlit.io) | Web UI and interaction |
| [OpenCV](https://opencv.org) | Image processing |
| [Pandas](https://pandas.pydata.org) | Color data handling |
| [NumPy](https://numpy.org) | Color math |
| [colorsys](https://docs.python.org/3/library/colorsys.html) | Color space conversions |
| [Pillow](https://python-pillow.org) | Image conversion |
| [streamlit-drawable-canvas](https://github.com/andfanilo/streamlit-drawable-canvas) | Interactive pixel clicks |

---

## 🗂 Dataset

This app uses the [codebrainz/color-names](https://github.com/codebrainz/color-names) dataset with 900+ color names and their RGB values.  
Live-loaded from GitHub for latest updates:  
```txt
https://raw.githubusercontent.com/codebrainz/color-names/master/output/colors.csv
````


## 🛠️ Setup Instructions

### 📦 Local Run

```bash
git clone https://github.com/North-Abyss/Color-Picker-App-KSY
cd Color-Picker-App-KSY
pip install -r requirements.txt
streamlit run app.py
```

### 🌐 Streamlit Cloud Deployment

Just push this repo to GitHub, connect to [streamlit.io/cloud](https://streamlit.io/cloud), and hit "Deploy App".

---

## 📁 Folder Structure

```
Color-Picker-App-KSY/
│
├── app.py               # Main Streamlit app
├── requirements.txt     # Dependencies
├── README.md            # This file
├── sample_images/       # Optional: images for demo
```

---

## 🙌 Acknowledgements

* Color dataset by [Codebrainz](https://github.com/codebrainz)
* Streamlit and open-source community for amazing tools

---

## 🏆 Built For Hackathons

Designed to be fast, intuitive, and helpful for:

* 🎨 Designers selecting brand-consistent colors
* 👩‍💻 Developers building UIs
* 🧑‍🔬 Accessibility analysts
* 🧠 Anyone needing pixel-perfect color insight

---

## 📬 Contact

Made with ❤️ by [North-Abyss](https://github.com/North-Abyss)
Questions or suggestions? Open an [issue](https://github.com/North-Abyss/Color-Picker-App-KSY/issues) or drop a ⭐ if you like it!

