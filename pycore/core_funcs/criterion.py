import json
from typing import Dict
from os import path


class TransformativeCriteria:
    def __init__(self, vals: Dict):
        self.width: int = int(vals.get('width', 1))
        self.height: int = int(vals.get('height'))
        self.resize_method: str = vals.get('resize_method', "BICUBIC").upper()
        self.flip_x: bool = vals.get("flip_x", False)
        self.flip_y: bool = vals.get("flip_y", False)
        self.rotation = int(vals['rotation'] or 0)

    def must_resize(self, orig_width: int, orig_height: int) -> bool:
        return self.width != orig_width or self.height != orig_height

    # def must_transform(orig_width: int, orig_height: int) -> Bool:
    #     return self.must_resize() or self.flip_x or self.flip_y or self.must_rotate()

    def must_rotate(self) -> bool:
        return self.rotation != 0


class CreationCriteria(TransformativeCriteria):
    """ Contains all of the criterias for Creating an animated image """
    def __init__(self, vals):
        super(CreationCriteria, self).__init__(vals)
        self.name: str = vals['name']
        self.fps: float = float(vals['fps'] or 0)
        self.delay: float = float(vals['delay'] or 0)
        self.extension: str = vals['format']
        self.reverse: bool = vals['is_reversed']
        self.preserve_alpha: bool = vals['preverse_alpha']
        self.loop_count = int(vals['loop_count'] or 0)
        self.start_frame = (int(vals['start_frame'] or 0) or 1)
        self.start_frame = self.start_frame - 1 if self.start_frame >= 0 else self.start_frame
        self.skip_frame = vals.get('skip_frame') or 0


class ModificationCriteria(CreationCriteria):
    """ Contains all of the criterias for Modifying the specifications of an animated image """

    def __init__(self, vals):
        self.orig_name = vals['orig_name']
        self.orig_base_name = path.splitext(self.orig_name)[0]
        self.orig_width = vals['orig_width']
        self.orig_height = vals['orig_height']
        self.orig_delay = vals['orig_delay']
        self.orig_frame_count = vals['orig_frame_count']
        self.orig_frame_count_ds = vals['orig_frame_count_ds']
        self.orig_loop_duration = vals['orig_loop_duration']
        self.orig_loop_count = int(vals['orig_loop_count'] or 0)
        self.orig_format = vals['orig_format']

        self.name = vals['name']
        self.width = int(vals.get('width') or 0)
        self.height = int(vals.get('height') or 0)
        self.delay = float(vals['delay'] or 0)
        self.fps = float(vals['fps'] or 0)
        self.loop_count = int(vals.get('loop_count') or 0)
        self.rotation = int(vals.get('rotation') or 0)
        self.format = vals['format']

        self.flip_x: bool = vals.get('flip_x')
        self.flip_y: bool = vals.get('flip_y')
        self.is_reversed = vals['is_reversed']
        self.preserve_alpha = vals['preserve_alpha']

    def renamed(self) -> bool:
        return self.orig_base_name != self.name

    def must_resize(self) -> bool:
        return self.orig_width != self.width or self.orig_height != self.height
    
    def must_rotate(self) -> bool:
        return bool(self.rotation)
    
    def must_redelay(self) -> bool:
        return self.orig_delay != self.delay

    def must_reloop(self) -> bool:
        return self.orig_loop_count != self.loop_count

    def must_flip(self) -> bool:
        return self.flip_x or self.flip_y

    def change_format(self) -> bool:
        return self.orig_format != self.format

    def gif_mustsplit_alteration(self) -> bool:
        altered = self.is_reversed or self.must_flip() or self.must_rotate()
        return altered

    def apng_mustsplit_alteration(self) -> bool:
        altered = self.must_resize() or self.must_rotate() or self.must_redelay() or self.must_reloop() or self.must_flip() or self.is_reversed
        return altered

    def orig_dimensions(self) -> str:
        return f"{self.orig_width}x{self.orig_height}"
        
    def dimensions(self) -> str:
        return f"{self.width}x{self.height}"




class SplitCriteria:
    """ Contains all of the criterias for Splitting an animated image """

    def __init__(self, vals):
        self.new_name: str = vals['new_name'].strip()
        if self.new_name.isspace():
            raise Exception("You should not rename the file as spaces!")
        self.pad_count: int = min(int(vals['pad_count'] or 0), 15)
        self.color_space: int = int(vals['color_space'] or 0)
        self.is_duration_sensitive: bool = vals['is_duration_sensitive']
        self.is_unoptimized: bool = vals['is_unoptimized']
        self.will_generate_delay_info: bool = vals['will_generate_delay_info']


class SpritesheetBuildCriteria:
    """ Contains all of the criterias to build a spritesheet """

    def __init__(self, vals: dict):
        self.tile_width: int = int(vals.get('tile_width') or 0)
        self.tile_height: int = int(vals.get('tile_height') or 0)
        self.input_format: str = vals['input_format']
        self.tiles_per_row: int = int(vals.get('tile_row') or 0)
        self.offset_x: int = int(vals.get('offset_x') or 0)
        self.offset_y: int = int(vals.get('offset_y') or 0)
        self.padding_x: int = int(vals.get('padding_x') or 0)
        self.padding_y: int = int(vals.get('padding_y') or 0)
        self.preserve_alpha: bool = vals['preserve_alpha']


class SpritesheetSliceCriteria:
    """ Contains all of the criterias to slice a spritesheet """

    def __init__(self, vals):
        self.sheet_width: int = int(vals.get('sheet_width') or 0)
        self.sheet_height: int = int(vals.get('sheet_height') or 0)
        self.tile_width: int = int(vals.get('tile_width') or 0)
        self.tile_height: int = int(vals.get('tile_height') or 0)
        self.offset_x: int = int(vals.get('offset_x') or 0)
        self.offset_y: int = int(vals.get('offset_y') or 0)
        self.padding_x: int = int(vals.get('padding_x') or 0)
        self.padding_y: int = int(vals.get('padding_y') or 0)
        self.is_edge_alpha: bool = vals.get('is_edge_alpha')


class GIFOptimizationCriteria:
    """ Criteria for GIF-related optimization/unoptimization """

    def __init__(self, vals):
        self.is_optimized = vals['is_optimized']
        self.optimization_level = vals['optimization_level']
        self.is_lossy = vals['is_lossy']
        self.lossy_value = int(vals['lossy_value'] or 0)
        self.is_reduced_color = vals['is_reduced_color']
        self.color_space = int(vals['color_space'] or 0)
        self.is_unoptimized = vals['is_unoptimized']


class GIFCreationCriteria:
    """ Criteria for creating GIFs alongside optimizations in one go """

    def __init__(self, vals):
        pass


class APNGOptimizationCriteria:
    """ Criteria for APNG-related optimization/unoptimization """

    def __init__(self, vals):
        self.is_optimized = vals['apng_is_optimized']
        self.optimization_level = int(vals.get('apng_optimization_level') or 0)
        self.is_lossy = vals['apng_is_lossy']
        self.lossy_value = int(vals.get('apng_lossy_value') or 0)
        self.is_unoptimized = vals['apng_is_unoptimized']
    
    def must_opt(self) -> bool:
        return (self.is_optimized and self.optimization_level) or (self.is_lossy and self.lossy_value)


class CriteriaBundle:
    """ Packs multiple criterias into one"""

    def __init__(self, vals):
        self.create_aimg_criteria: CreationCriteria = vals.get('create_aimg_criteria')
        self.split_aimg_criteria: SplitCriteria = vals.get('split_aimg')
        self.modify_aimg_criteria: ModificationCriteria = vals.get('modify_aimg')
        # self.build_spr: SpritesheetBuildCriteria = vals.get('build_spr')
        # self.slice_spr: SpritesheetSliceCriteria = vals.get('slice_spr')
        self.gif_opt_criteria: GIFOptimizationCriteria = vals.get('gif_opt_criteria')
        self.apng_opt_criteria: APNGOptimizationCriteria = vals.get('apng_opt_criteria')
