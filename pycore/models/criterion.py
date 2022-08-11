from fractions import Fraction
import math
from pycore.core_funcs import stdio
from pycore.models.image_formats import ImageFormat
from pycore.models.metadata import ImageMetadata, AnimatedImageMetadata
from pycore.models.enums import ALPHADITHER
from typing import Dict, List, Tuple, Any, Optional


from enum import Enum, unique


@unique
class DelayHandling(Enum):
    DO_NOTHING = 0
    EVEN_OUT = 1
    MULTIPLY_AVERAGE = 2

class CriteriaBase:
    pass


class TransformativeCriteria(CriteriaBase):
    def __init__(self, vals: Dict):
        self.width: int = int(vals.get("width", 1))
        self.height: int = int(vals.get("height"))
        self.resize_method: str = (vals.get("resize_method") or "BICUBIC").upper()
        self.flip_x: bool = vals.get("flip_x", False)
        self.flip_y: bool = vals.get("flip_y", False)
        self.rotation = int(vals["rotation"] or 0)

    @property
    def size(self) -> Tuple[int, int]:
        return self.width, self.height

    def must_resize(self, metadata: Optional[ImageMetadata] = None, width: Optional[int] = 0,
                    height: Optional[int] = 0) -> bool:
        if metadata:
            return self.width != metadata.width["value"] or self.height != metadata.height["value"]
        else:
            return self.width != width or self.height != height

    def must_flip(self):
        return self.flip_x or self.flip_y

    # def must_transform(orig_width: int, orig_height: int) -> Bool:
    #     return self.must_resize() or self.flip_x or self.flip_y or self.must_rotate()

    # def must_rotate(self) -> bool:
    #     return self.rotation != 0


class CreationCriteria(TransformativeCriteria):
    """ Contains all of the criterias for Creating an animated image """

    def __init__(self, vals):
        super(CreationCriteria, self).__init__(vals)
        # self.name: str = vals["name"]
        self.fps: float = float(vals["fps"] or 10) or 10
        self.delay: float = float(vals["delay"] or 0.1) or 0.1
        self.format: ImageFormat = ImageFormat[str.upper(vals["format"])]
        self.reverse: bool = vals["is_reversed"]
        self.preserve_alpha: bool = vals["preserve_alpha"]
        self.loop_count = int(vals["loop_count"] or 0)
        start_frame_val = int(vals["start_frame"] or 0) or 1
        self.start_frame = start_frame_val - 1 if start_frame_val >= 0 else start_frame_val
        self.skip_frame = vals.get("skip_frame") or 0


class ModificationCriteria(CreationCriteria):
    """ Contains all of the criterias for Modifying the specifications of an animated image """

    def __init__(self, vals):
        self.hash_sha1 = vals["hash_sha1"]
        self.last_modified_dt = vals["last_modified_dt"]
        self.delay_handling = DelayHandling[str.upper(vals["delay_handling"])]

        super(ModificationCriteria, self).__init__(vals)

    def change_format(self, metadata: ImageMetadata):
        stdio.error(f'{metadata.format["value"]} {self.format.name}')
        return str.upper(metadata.format["value"]) != self.format.name

    def must_resize(self, metadata: Optional[AnimatedImageMetadata] = None, width: Optional[int] = 0,
                    height: Optional[int] = 0) -> bool:
        """Checks whether or not the animated image needs to be resized

        Args:
            metadata (Optional[AnimatedImageMetadata], optional): _description_. Animated image metadata.
            width (Optional[int], optional): _description_. Original width of the image.
            height (Optional[int], optional): _description_. Original height of an image.

        Returns:
            bool: True if the animated image needs to be resized, else False.
        """
        return super(ModificationCriteria, self).must_resize(metadata, width, height)

    def must_transform(self, metadata: AnimatedImageMetadata) -> bool:
        """Check whether or not pixel transformation must be performed to the animated image 

        Args:
            metadata (AnimatedImageMetadata): The metadata of the animated image

        Returns:
            bool: True if the animated image must be pixel-transformed, else False.
        """
        return self.must_resize(metadata) or self.must_flip()

    def apng_must_reiterate(self, metadata: AnimatedImageMetadata) -> bool:
        return self.must_resize(metadata) or self.must_flip() or self.must_redelay(metadata) or self.reverse

    def must_redelay(self, metadata: Optional[AnimatedImageMetadata] = None, delays: Optional[List[float]] = None,
                     delay: Optional[float] = None):
        if metadata:
            return metadata.average_delay["value"] != self.delay
        elif delays:
            return sum(delays) / len(delays) != self.delay
        elif delay:
            return delay != self.delay
        
    def calculate_new_delay(self, metadata: AnimatedImageMetadata):
        orig_delays = metadata.delays["value"]
        new_delays: List
        if self.delay_handling == DelayHandling.EVEN_OUT:
            new_delays = [Fraction(self.delay).limit_denominator() for _ in orig_delays]
        elif self.delay_handling == DelayHandling.MULTIPLY_AVERAGE:
            orig_avg_delay = sum(orig_delays) / len(metadata.delays)
            delay_ratio = Fraction(self.delay).limit_denominator() / orig_avg_delay
            stdio.error(f"delay ratio {delay_ratio}, {self.delay}, {Fraction(self.delay).limit_denominator()}, {orig_avg_delay}")
            new_delays = [delay_ratio * od for od in orig_delays]
        elif self.delay_handling == DelayHandling.DO_NOTHING:
            new_delays = orig_delays
        else:
            raise Exception(f"Unknown delay handling method: {self.delay_handling}")
        return new_delays

    def must_reloop(self, metadata: Optional[AnimatedImageMetadata] = None, loop_count: Optional[int] = 0):
        if metadata:
            return metadata.loop_count["value"] != self.loop_count
        else:
            return loop_count != self.loop_count

    def project_modifications_list(self, image_obj: Any) -> List[Dict]:
        return [image_obj, self.start_frame]

    # def gif_must_split(self) -> bool:
    #     altered = self.reverse or self.flip_x or self.flip_y or self.rotation
    #     return altered

    def orig_dimensions(self) -> str:
        return f"{self.orig_width}x{self.orig_height}"

    def dimensions(self) -> str:
        return f"{self.width}x{self.height}"


class SplitCriteria(CriteriaBase):
    """ Contains all of the criterias for Splitting an animated image """

    def __init__(self, vals):
        self.new_name: str = vals["new_name"].strip()
        if self.new_name.isspace():
            raise Exception("You should not rename the file as spaces!")
        self.pad_count: int = min(int(vals["pad_count"] or 0), 15)
        self.color_space: int = int(vals["color_space"] or 0)
        # self.is_duration_sensitive: bool = vals["is_duration_sensitive"]
        self.is_unoptimized: bool = vals["is_unoptimized"]
        self.convert_to_rgba: bool = vals["convert_to_rgba"]
        self.extract_delay_info: bool = vals["extract_delay_info"]


class SpritesheetBuildCriteria(CriteriaBase):
    """ Contains all of the criterias to build a spritesheet """

    def __init__(self, vals: dict):
        self.tile_width: int = int(vals.get("tile_width") or 0)
        self.tile_height: int = int(vals.get("tile_height") or 0)
        self.input_format: str = vals["input_format"]
        self.tiles_per_row: int = int(vals.get("tile_row") or 0)
        self.offset_x: int = int(vals.get("offset_x") or 0)
        self.offset_y: int = int(vals.get("offset_y") or 0)
        self.padding_x: int = int(vals.get("padding_x") or 0)
        self.padding_y: int = int(vals.get("padding_y") or 0)
        self.preserve_alpha: bool = vals["preserve_alpha"]


class SpritesheetSliceCriteria(CriteriaBase):
    """ Contains all of the criterias to slice a spritesheet """

    def __init__(self, vals):
        self.sheet_width: int = int(vals.get("sheet_width") or 0)
        self.sheet_height: int = int(vals.get("sheet_height") or 0)
        self.tile_width: int = int(vals.get("tile_width") or 0)
        self.tile_height: int = int(vals.get("tile_height") or 0)
        self.offset_x: int = int(vals.get("offset_x") or 0)
        self.offset_y: int = int(vals.get("offset_y") or 0)
        self.padding_x: int = int(vals.get("padding_x") or 0)
        self.padding_y: int = int(vals.get("padding_y") or 0)
        self.is_edge_alpha: bool = vals.get("is_edge_alpha")


class GIFOptimizationCriteria(CriteriaBase):
    """ Criteria for GIF-related optimization/unoptimization """

    def __init__(self, vals):
        self.is_optimized = vals["is_optimized"]
        self.optimization_level = vals["optimization_level"]
        self.is_lossy = vals["is_lossy"]
        self.lossy_value = int(vals["lossy_value"] or 0)
        self.is_reduced_color = vals["is_reduced_color"]
        self.color_space = int(vals["color_space"] or 0)
        self.is_unoptimized = vals["is_unoptimized"]
        self.dither_method = (vals["dither_method"] or "FLOYD_STEINBERG").upper()
        self.palletization_method = (vals["palletization_method"] or "ADAPTIVE").upper()
        self.is_dither_alpha = vals["is_dither_alpha"]
        self.dither_alpha_method = (vals.get("dither_alpha_method") or "SCREENDOOR").upper()
        self.dither_alpha_threshold = int(vals["dither_alpha_threshold"]) or 0

    @property
    def dither_alpha_method_enum(self) -> ALPHADITHER:
        return ALPHADITHER[self.dither_alpha_method]

    @property
    def dither_alpha_threshold_value(self) -> int:
        return math.floor(256 * self.dither_alpha_threshold / 100)


# class GIFCreationCriteria:
#     """ Criteria for creating GIFs alongside optimizations in one go """
#
#     def __init__(self, vals):
#         pass


class APNGOptimizationCriteria(CriteriaBase):
    """ Criteria for APNG-related optimization/unoptimization """

    def __init__(self, vals):
        self.is_optimized = vals["apng_is_optimized"]
        self.optimization_level = int(vals.get("apng_optimization_level") or 0)
        self.is_reduced_color = vals["apng_is_reduced_color"]
        self.color_count = int(vals.get("apng_color_count") or 0)
        self.quantization_enabled = vals["apng_quantization_enabled"]
        self.quantization_quality_min = int(vals.get("apng_quantization_quality_min") or 0)
        self.quantization_quality_max = int(vals.get("apng_quantization_quality_max") or 0)
        self.quantization_speed = int(vals.get("apng_quantization_speed") or 0)
        self.is_unoptimized = vals["apng_is_unoptimized"]
        self.convert_color_mode = vals["apng_convert_color_mode"]
        self.new_color_mode = vals.get("apng_new_color_mode") or ""

    def must_opt(self) -> bool:
        return (self.is_optimized and self.optimization_level) or (self.is_reduced_color and self.color_count)


class CriteriaBundle(CriteriaBase):
    """ Packs multiple criterias into one"""

    def __init__(self, vals):
        self.create_aimg_criteria: CreationCriteria = vals.get("create_aimg_criteria")
        self.split_aimg_criteria: SplitCriteria = vals.get("split_aimg_criteria")
        self.modify_aimg_criteria: ModificationCriteria = vals.get("modify_aimg_criteria")
        # self.build_spr: SpritesheetBuildCriteria = vals.get('build_spr')
        # self.slice_spr: SpritesheetSliceCriteria = vals.get('slice_spr')
        self.gif_opt_criteria: GIFOptimizationCriteria = vals.get("gif_opt_criteria")
        self.apng_opt_criteria: APNGOptimizationCriteria = vals.get("apng_opt_criteria")
