import sys
from pathlib import Path
from . import stdio


class UnidentifiedImageException(Exception):
    """Raised when an image cannot be recognized by Pillow"""

    def __init__(
        self,
        image_path: Path,
        message: str = "The file {image_path} cannot be identified as a valid image file",
    ) -> None:
        """Initialize the exception

        Args:
            image_path (str): Path to the image
            message (str, optional): Exception message. Defaults to "The file {image_path} cannot be identified as a
            valid image file".
        """
        self.image_path = image_path
        self.message = message.format(image_path=self.image_path)
        super().__init__(self.message)


class ImageNotStaticException(Exception):
    """Raised when an image is expected to be static, but is not."""

    def __init__(
        self,
        image_name: str,
        extension: str,
        message: str = "The image {image_name} is not a static {extension}",
    ) -> None:
        """Initialize the exception

        Args:
            image_name (str): Name of the image
            extension (str): Capitalized extension
            message (str, optional): Exception message. Defaults to "The image {image_name} is not a static
            {extension}".
        """
        self.image_name = image_name
        self.extension = extension
        self.message = message.format(image_name=self.image_name, extension=self.extension)
        super().__init__(self.message)


class ImageNotAnimatedException(Exception):
    """Raised when an image is expected to be animated, but is not."""

    def __init__(
        self,
        image_name: str,
        extension: str,
        message: str = "The image {image_name} is not an animated {extension}",
    ) -> None:
        """Initialize the exception

        Args:
            image_name (str): Name of the image
            extension (str): Capitalized extension
            message (str, optional): Exception message. Defaults to "The image {image_name} is not an animated
            {extension}".
        """
        self.image_name = image_name
        self.extension = extension
        self.message = message.format(image_name=self.image_name, extension=self.extension)
        super().__init__(self.message)


class UnsupportedImageModeException(Exception):
    """Raised when an image is expected to be in a certain color mode, but is not."""

    def __init__(
        self,
        image_name: str,
        color_mode: str,
        message: str = "The image {image_name}'s color mode {color_mode} is not supported for this operation",
    ) -> None:
        """Initialize the exception

        Args:
            image_name (str): Name of the image
            color_mode (str): Color mode
            message (str, optional): Exception message. Defaults to "The image {image_name} is not an animated
            {extension}".
        """
        self.image_name = image_name
        self.color_mode = color_mode
        self.message = message.format(image_name=self.image_name, extension=self.color_mode)
        super().__init__(self.message)


class MalformedCommandException(Exception):
    """Raised when a imager command is malformed."""

    def __init__(
        self,
        imager_name: str,
        message="The command passed for the imager {imager_name} is malformed!",
    ) -> None:
        """Initialize the exception

        Args:
            imager_name (str): Name of the imager that the command is built for.
            message (str, optional): [description]. Defaults to "The command passed for the imager {imager_name} is
            malformed!".
        """
        self.imager_name = imager_name
        self.message = message.format(imager_name=imager_name)
        super().__init__(self.message)


class UnsupportedPlatformException(Exception):
    """Raised when a certain operation is not supported in the specified platform"""

    def __init__(self, platform, message="The platform {platform_name} does not support this operation") -> None:
        self.platform = platform
        self.message = message.format(platform_name=platform)
        super().__init__(self.message)


def set_exception_handler(json_mode: bool = True):
    """Toggle between normal python verbose traceback print, or json-serialzied traceback and error prints

    Args:
        json_mode (bool, optional): True = JSON python traceback; False = Normal error message. Defaults to True.
    """

    def exception_handler(exception_type, exception, traceback, debug_hook=sys.excepthook):
        if json_mode:
            stdio.error_traceback(traceback)
            stdio.error(f"Error: {exception}")
        else:
            debug_hook(exception_type, exception, traceback)

    sys.excepthook = exception_handler
