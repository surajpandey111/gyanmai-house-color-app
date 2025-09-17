from PIL import Image

def load_image(file):
    return Image.open(file).convert("RGB")

def save_image(image, path):
    image.save(path, format="PNG")
