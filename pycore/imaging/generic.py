from PIL import Image
from PIL.Image import Resampling
from pycore.core_funcs import stdio
from pycore.models.criterion import TransformativeCriteria


def transform_image(im: Image.Image, criteria: TransformativeCriteria) -> Image.Image:
    """
    Perform general transformations to an image (resizing, flipping and rotation) based on the supplied criteria
    Args:
        im (Image.Image): Pillow image
        criteria (TransformativeCriteria): Criteria needed for transforming the image

    Returns:

    """
    orig_width, orig_height = im.size
    if criteria.flip_x:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    if criteria.flip_y:
        im = im.transpose(Image.FLIP_TOP_BOTTOM)
    if criteria.must_resize(width=orig_width, height=orig_height):
        resize_method_enum = getattr(Resampling, criteria.resize_method)
        # yield {"resize_method_enum": resize_method_enum}
        im = im.resize(
            (round(criteria.width), round(criteria.height)),
            resample=resize_method_enum,
        )
    return im
