from enum import Enum, unique

@unique
class ALPHADITHER(int, Enum):
    """Options for different transparency dithering methods"""

    # Screen door transparency pattern inspired from
    # https://digitalrune.github.io/DigitalRune-Documentation/html/fa431d48-b457-4c70-a590-d44b0840ab1e.htm
    SCREENDOOR: int = 0
    DIFFUSION: int = 1  # Not implemented yet
    NOISE: int = 2  # Not implemented yet
