from io import BytesIO
from PIL import Image
from PIL.ImageFilter import BLUR, CONTOUR, SHARPEN


def blur(bytes_: str) -> None:
    image = Image.open('tmp.jpeg')
    image.filter(BLUR).save('tmp_filtered.jpeg')


def contour(bytes_: str) -> Image:
    image = Image.open(BytesIO(bytes_))
    return image.filter(CONTOUR)


def sharpen(bytes_: str) -> Image:
    image = Image.open(BytesIO(bytes_))
    return image.filter(SHARPEN)
