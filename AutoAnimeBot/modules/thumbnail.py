import random
from PIL import Image, ImageOps, ImageFilter
from string import ascii_uppercase, digits
import os
import requests


def make_col():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


async def generate_thumbnail(id, file, title, ep_num, size, dur):
    # Download the thumbnail from the specified link
    thumbnail_url = "https://ibb.co/k9h6PBZ"
    r = requests.get(thumbnail_url, stream=True)
    r.raise_for_status()

    # Save the thumbnail as a temporary image file (JPG format)
    thumbnail_path = "./" + "".join(random.choices(ascii_uppercase + digits, k=10)) + ".jpg"
    with open(thumbnail_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

    border = make_col()
    image = Image.open(thumbnail_path)
    image = image.convert("RGBA")
    image = image.resize((1280, 720))

    image2 = image.filter(filter=ImageFilter.GaussianBlur(10))
    black = Image.new("RGB", (1280, 720), "black").convert("RGBA")
    image2 = Image.blend(image2, black, 0.5)

    image2 = ImageOps.expand(image2, 20, border)
    image2 = image2.resize((1280, 720))

    ldraw = ImageDraw.Draw(image2)
    line = [(0, 0), (50, 720)]
    ldraw.line(line, border, 20)

    image2.thumbnail((1280, 720))
    w, h = image2.size

    thumb = (
        "./downloads/"
        + "".join(random.choices(ascii_uppercase + digits, k=10))
        + ".jpg"
    )
    image2.save(thumb)

    try:
        os.remove(thumbnail_path)
    except:
        pass

    return thumb, w, h
