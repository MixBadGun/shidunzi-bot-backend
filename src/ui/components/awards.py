import io
from pathlib import Path

import PIL
import PIL.Image
from imagetext_py import TextAlign
from loguru import logger

from src.ui.base.basics import Fonts
from src.ui.base.tools import hex_to_rgb, mix_color, rgb_to_hex

from ..base.basics import (
    apply_mask,
    draw_rounded_rectangle,
    paste_image,
    render_text,
    rounded_rectangle_mask,
)

DISPLAY_BOX_CACHE: dict[str, PIL.Image.Image] = {}


def _display_box(
    color: str, central_image: str | bytes | Path | PIL.Image.Image
) -> PIL.Image.Image:
    if not isinstance(central_image, (str, Path, PIL.Image.Image)):
        image = PIL.Image.open(io.BytesIO(central_image)).convert("RGBA")
    elif isinstance(central_image, PIL.Image.Image):
        image = central_image.convert("RGBA")
    else:
        image = PIL.Image.open(central_image).convert("RGBA")
        logger.info(f"图片 {central_image} 还没有被预渲染过，现在渲染。")
    image = image.resize((180, 144), PIL.Image.ADAPTIVE)
    image = apply_mask(image, rounded_rectangle_mask(180, 144, 10))

    canvas = PIL.Image.new("RGBA", (180, 144), (255, 255, 255, 0))

    outerRect = draw_rounded_rectangle(
        180, 144, 10, rgb_to_hex(mix_color(hex_to_rgb(color), (255, 255, 255), 0.35))
    )
    innerRect = draw_rounded_rectangle(176, 140, 8, color)

    paste_image(canvas, outerRect, 0, 0)
    paste_image(canvas, innerRect, 2, 2)
    paste_image(canvas, image, 0, 0)

    return canvas


def display_box_raw(color: str, image: PIL.Image.Image | Path | str | bytes):
    """
    渲染 DisplayBox
    """

    if not isinstance(image, PIL.Image.Image):
        cache_key = f"{color}-{hash(image)}"
        if cache_key not in DISPLAY_BOX_CACHE:
            DISPLAY_BOX_CACHE[cache_key] = _display_box(color, image)
        image = DISPLAY_BOX_CACHE[cache_key].copy()
    else:
        image = _display_box(color, image)
    return image


def ref_book_box_raw(
    color: str,
    image: Path,
    notation_bottom: str,
    name: str,
    name_bottom: str,
    sold_out: bool = False,
) -> PIL.Image.Image:
    box = display_box_raw(color, image)

    if sold_out:
        so = PIL.Image.open("./res/sold_out.png")
        so = so.convert("RGBA")
        paste_image(box, so, 0, 0)

    bl_notation = render_text(
        text=notation_bottom,
        width=170,
        color="#FFFFFF",
        font=Fonts.MARU_MONICA,
        font_size=36,
        stroke=2,
        stroke_color="#000000",
        margin_bottom=5,
        margin_left=5,
    )

    title = render_text(
        text=name,
        width=180,
        align=TextAlign.Center,
        color="#FFFFFF",
        font=Fonts.HARMONYOS_SANS_BLACK,
        font_size=26,
    )
    title2 = render_text(
        text=name_bottom,
        width=180,
        color="#C4BEBD",
        font=Fonts.HARMONYOS_SANS_BLACK,
        font_size=20,
        align=TextAlign.Center,
    )

    block = PIL.Image.new("RGBA", (216, 210), "#9B9690")
    paste_image(block, box, 18, 18)
    paste_image(block, title, 18, 170)
    paste_image(block, title2, 18, 194)
    paste_image(block, bl_notation, 23, 117)

    return block
