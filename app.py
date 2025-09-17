import streamlit as st
from gyanmai.utils.image_io import load_image, save_image
from gyanmai.utils.color_ops import recolor_house
from gyanmai.utils.segmentation import extract_house, merge_recolor
from gyanmai import branding
import os
import cv2
import numpy as np
from PIL import Image

# Branding / header
branding.show_header()

# Upload image
uploaded = st.file_uploader("📤 Upload your house image", type=["png", "jpg", "jpeg"])

# Color picker
color = st.color_picker("🎨 Pick a color for walls", "#749CAA")

# Model selection
model_options = ["u2net", "u2netp", "isnet-general-use"]
selected_model = st.sidebar.selectbox("Select Segmentation Model", model_options)

# Enhance image option
enhance = st.checkbox("Enhance Image?")

if uploaded:
    # Load image
    image = load_image(uploaded)

    # Preprocess if enabled
    if enhance:
        try:
            # Convert PIL image to OpenCV format
            img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            # Enhance contrast (CLAHE)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            lab = cv2.cvtColor(img_cv, cv2.COLOR_BGR2LAB)
            lab[:,:,0] = clahe.apply(lab[:,:,0])
            img_cv = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
            # Sharpen edges
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            img_cv = cv2.filter2D(img_cv, -1, kernel)
            # Convert back to PIL image
            image = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
        except Exception as e:
            st.error(f"Error during image enhancement: {e}")
            image = load_image(uploaded)  # Fallback to original if preprocessing fails

    # Step 1: Extract only house (foreground)
    house_only = extract_house(image, selected_model)

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

# Footer branding
st.markdown(
    """
    ---
    👨‍💻 Developed by **Suraj Kumar Pandey**  
    🎓 Under mentorship of **Dr. Tauseef Ahmad (HOD IT)**  
    """,
    unsafe_allow_html=True
)