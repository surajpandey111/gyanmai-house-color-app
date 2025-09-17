# gyanmai/utils/segmentation.py

from rembg import new_session, remove
from PIL import Image
import numpy as np
import cv2

def extract_house(image: Image.Image, model_name: str = "isnet-general-use") -> Image.Image:
    """
    Extracts house (foreground) from background using rembg with a specific model and refines mask.
    """
    # Initialize session with the specified model
    session = new_session(model_name)
    # Perform removal using the session
    rough_fg = remove(image, session=session)
    data = np.array(rough_fg)

    # Refine mask
    alpha = data[:, :, 3]
    kernel = np.ones((3,3), np.uint8)
    alpha = cv2.morphologyEx(alpha, cv2.MORPH_CLOSE, kernel)
    alpha = cv2.morphologyEx(alpha, cv2.MORPH_OPEN, kernel)
    alpha = cv2.GaussianBlur(alpha, (5,5), 0)
    data[:, :, 3] = alpha
    return Image.fromarray(data, "RGBA")

def merge_recolor(original: Image.Image, recolored: Image.Image) -> Image.Image:
    """
    Merges recolored house with original background.
    """
    bg = original.convert("RGBA")
    fg = recolored.convert("RGBA")
    combined = Image.alpha_composite(bg, fg)
    return combined