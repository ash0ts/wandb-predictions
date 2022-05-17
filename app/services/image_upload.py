from io import BytesIO

from PIL import Image


def read_imagefile(file) -> Image.Image:
    image = Image.open(BytesIO(file))
    return image
