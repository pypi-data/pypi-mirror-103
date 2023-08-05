from typing import Tuple
"""
Config rectangle, pillow font, size, colours 
"""


class DrawConfig:
    COLOUR_RECTANGLE: Tuple[int, int, int, int] = (0, 255, 0, 127)
    COLOUR_FONT: Tuple[int, int, int, int] = (200, 0, 0, 0)
    FONT_FILE: str = "arial.ttf"
    FONT_SIZE: int = 48
    FONT_X_STEP_POS: int = 0
    FONT_Y_STEP_POS: int = 0
