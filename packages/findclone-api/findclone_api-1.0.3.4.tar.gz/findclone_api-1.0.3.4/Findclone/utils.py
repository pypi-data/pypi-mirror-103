from random import sample
from string import ascii_letters, digits

from PIL import Image, ImageDraw, ImageFont
from io import BytesIO, BufferedReader
from .models import Profiles
from Findclone.pillow_config import DrawConfig


def paint_boxes(file: [BufferedReader, bytes], face_boxes: dict) -> BytesIO:
    """Drawing squares and face number in the image if more than 2 faces are found
    :return img_byte_arr: image BytesIO object
    """
    conf = DrawConfig
    font_file: str = conf.FONT_FILE
    font_size: int = conf.FONT_SIZE
    colour_f: tuple = conf.COLOUR_FONT
    colour_r: tuple = conf.COLOUR_RECTANGLE
    x = conf.FONT_X_STEP_POS
    y = conf.FONT_Y_STEP_POS
    img = Image.open(file) if isinstance(file, BufferedReader) else Image.open(BytesIO(file))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font=font_file, size=font_size)
    for face_box in face_boxes["faceBoxes"]:
        face_number = str(face_box["i"])
        height = face_box["h"]
        _l = face_box["l"]
        t = face_box["t"]
        draw.rectangle(((_l, t), (_l + height, t + height)), outline=colour_r, width=3)
        draw.text(((_l*2+height + x)/2, t+height + y), str(face_number), fill=colour_f, font=font)
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format="png")
    del conf
    return img_byte_arr


def random_string(word: int = 8): return "".join(sample(ascii_letters + digits, word))


def is_image(obj: [Profiles, BytesIO]) -> bool:
    """Check response if is image"""
    return isinstance(obj, BytesIO)


def save_image(img: BytesIO, filename: str) -> None:
    """
    Args:
        img: BytesIO object
        filename: path file
    """
    with open(filename, "wb") as file:
        file.write(img.getvalue())
