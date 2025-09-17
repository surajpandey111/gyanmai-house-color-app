# gyanmai/utils/segmentation.py

from rembg import remove
from PIL import Image
import numpy as np

def extract_house(image: Image.Image) -> Image.Image:
    """
    Extracts house (foreground) from background using rembg.
    Returns a transparent PNG of house only.
    """
    return remove(image)

def merge_recolor(original: Image.Image, recolored: Image.Image) -> Image.Image:
    """
    Merges recolored house with original background.
    """
    bg = original.convert("RGBA")
    fg = recolored.convert("RGBA")
    combined = Image.alpha_composite(bg, fg)
    return combined
