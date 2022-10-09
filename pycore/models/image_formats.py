from enum import Enum, unique


@unique
class ImageFormat(Enum):
    GIF = 0
    PNG = 1


GIF_DELAY_DECIMAL_PRECISION = 3
APNG_DELAY_DECIMAL_PECISION = 4
