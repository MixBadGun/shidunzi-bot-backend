from dataclasses import dataclass
import enum
import os
from typing import Literal

import PIL
import PIL.ImageDraw
import PIL.ImageFont

from ..threading import make_async

from .typing import PillowColorLikeWeak, PILImage, PillowColorLikeStrong


class HorizontalAnchor(enum.Enum):
    left = 'l'
    middle = 'm'
    right = 'r'
    baseline = 's'


class VerticalAnchor(enum.Enum):
    ascender = 'a'
    top = 't'
    middle = 'm'
    baseline = 's'
    bottom = 'b'
    descender = 'd'


@dataclass
class TextBox:
    left: int
    top: int
    right: int
    bottom: int


FONT_BASE = os.path.join(".", "res", "catch", "fonts")


def _res(fn: str):
    return os.path.join(FONT_BASE, fn)


class Fonts(enum.Enum):
    FONT_HARMONYOS_SANS = _res("HarmonyOS_Sans_SC_Regular.ttf")
    FONT_HARMONYOS_SANS_BLACK = _res("HarmonyOS_Sans_SC_Black.ttf")
    ALIMAMA_SHU_HEI = _res("AlimamaShuHeiTi-Bold.ttf")
    JINGNAN_BOBO_HEI = _res("荆南波波黑-Bold.ttf")
    JIANGCHENG_YUANTI = _res("江城圆体 500W.ttf")


def textFont(fontEnum: Fonts, fontSize: int):
    return PIL.ImageFont.FreeTypeFont(fontEnum.value, fontSize)


DEFAULT_FONT = textFont(Fonts.FONT_HARMONYOS_SANS, 12)


@make_async
def drawText(
    draw: PIL.ImageDraw.ImageDraw,
    text: str,
    x: float,
    y: float,
    color: PillowColorLikeStrong,
    font=DEFAULT_FONT,
    strokeColor: PillowColorLikeStrong = 0,
    strokeWidth: int = 0,
    horizontalAlign: HorizontalAnchor = HorizontalAnchor.left,
    verticalAlign: VerticalAnchor = VerticalAnchor.top
):
    draw.text(
        (x, y),
        text,
        fill=color,
        font=font,
        stroke_fill=strokeColor,
        stroke_width=strokeWidth,
        anchor=horizontalAlign.value + verticalAlign.value
    )


def textBox(text: str, font: PIL.ImageFont.FreeTypeFont = DEFAULT_FONT):
    left, top, right, bottom = font.getbbox(text)

    return TextBox(left, top, right, bottom)
