from enum import IntEnum

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 650
FPS = 50
NUMBER_HAND_LANDMARKS = 21

MOUTH_LANDMARKS = [
    # Outer lips (clockwise)
    61, 185, 40, 39, 37, 0, 267, 269, 270, 409,
    291, 375, 321, 405, 314, 17, 84, 181, 91, 146,

    # Inner lips (clockwise)
    78, 191, 80, 81, 82, 13, 312, 311, 310, 415,
    308, 324, 318, 402, 317, 14, 87, 178, 88, 95,

    # Additional key points for mouth tracking
    62, 76, 184, 74, 73, 72, 11, 302, 303, 304
]

class Face(IntEnum):
    NORMAL = 0
    BLOW = 1


class Gesture(IntEnum):
    POINTER = 0
    OPEN = 1
    CLOSE = 2
    CLICK_START = 3
    CLICK_END = 4