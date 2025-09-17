import streamlit as st
from gyanmai.utils.image_io import load_image, save_image
from gyanmai.utils.color_ops import recolor_house
from gyanmai.utils.segmentation import extract_house, merge_recolor
from gyanmai import branding
import os

# Branding / header
branding.show_header()

# Upload image
uploaded = st.file_uploader("📤 Upload your house image", type=["png", "jpg", "jpeg"])

# Color picker
color = st.color_picker("🎨 Pick a color for walls", "#ff0000")

if uploaded:
    # Load image
    image = load_image(uploaded)

    # Step 1: Extract only house (foreground)
    house_only = extract_house(image)

    # Step 2: Apply recoloring to the house
    recolored_house = recolor_house(house_only, color)

    # Step 3: Merge recolored house with original background
    final = merge_recolor(image, recolored_house)

    # Show side-by-side preview
    st.subheader("🔍 Preview")
    st.image([image, final], caption=["Original", "Recolored"], use_container_width=True)

    # Save output
    os.makedirs("outputs", exist_ok=True)
    out_path = os.path.join("outputs", "recolored.png")
    save_image(final, out_path)

    # Download button
    with open(out_path, "rb") as file:
        st.download_button(
            label="⬇️ Download Recolored Image",
            data=file,
            file_name="gyanmai_recolored.png",
            mime="image/png"
        )
