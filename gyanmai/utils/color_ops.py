import numpy as np
from PIL import Image

def hex_to_rgb(hex_color: str):
    """Convert HEX (#rrggbb) to RGB tuple"""
    hex_color = hex_color.lstrip("#")
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return (r, g, b)

def recolor_house(image: Image.Image, hex_color: str) -> Image.Image:
    """
    Recolors the non-transparent parts of the house-only image.
    Works together with rembg mask.
    """
    img = image.convert("RGBA")
    data = np.array(img)

    # Convert HEX to RGB
    r, g, b = hex_to_rgb(hex_color)

    # Apply color only where alpha > 0 (house pixels)
    mask = data[:, :, 3] > 0
    data[mask, 0] = r
    data[mask, 1] = g
    data[mask, 2] = b

    return Image.fromarray(data, "RGBA")

