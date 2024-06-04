import PIL
import PIL.Image


PILLOW_COLOR_LIKE_STRONG = str | int | tuple[int, int, int] | tuple[int, int, int, int] | None
PILLOW_COLOR_LIKE = int | tuple[int] | tuple[int, int] | tuple[int, int, int] | tuple[int, int, int, int] | str | float | tuple[float]
PILLOW_COLOR_LIKE_WEAK = PILLOW_COLOR_LIKE | None

IMAGE = PIL.Image.Image