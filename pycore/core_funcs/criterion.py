class CreationCriteria:
    """ Contains all of the criterias for Creating an animated image """
    def __init__(self, vals):
        self.name: str = vals['name']
        self.fps: float = float(vals['fps'] or 0)
        self.delay: float = float(vals['delay'] or 0)
        self.extension: str = vals['format']
        self.reverse: bool = vals['is_reversed']
        self.transparent: bool = vals['is_transparent']
        self.flip_h: bool = vals['flip_x']
        self.flip_v: bool = vals['flip_y']
        self.resize_width = int(vals['width'] or 1)
        self.resize_height = int(vals['height'] or 1)
        self.resize_method = vals.get('resize_method', "BICUBIC")
        self.loop_count = int(vals['loop_count'] or 0)
        self.rotation = int(vals['rotation'] or 0)
    
    # def transform(self, resize_width, resize_height, flip_h, flip_v):
    #     try:
    #         resize_width = float(resize_width)
    #         resize_height = float(resize_height)
    #     except Exception as e:
    #         raise Exception(e)        
    #     self.resize_width: int = resize_width
    #     self.resize_height: int = resize_height
    #     self.flip_h = flip_h
    #     self.flip_v = flip_v
    #     return self


class SplitCriteria:
    """ Contains all of the criterias for Splitting an animated image """

    def __init__(self, json_vals):
        self.new_name: str = json_vals['new_name']
        self.pad_count: int = int(json_vals['pad_count'] or 0)
        self.color_space: int = int(json_vals['color_space'] or 0)
        self.is_duration_sensitive: bool = json_vals['is_duration_sensitive']
        self.is_unoptimized: bool = json_vals['is_unoptimized']
        self.will_generate_delay_info: bool = json_vals['will_generate_delay_info']


class ModificationCriteria:
    """ Contains all of the criterias for Modifying the specifications of an animated image """

    def __init__(self, json_vals):
        self.orig_name = json_vals['orig_name']
        self.name = json_vals['name']
        self.orig_width = json_vals['orig_width']
        self.orig_height = json_vals['orig_height']
        self.width = int(json_vals.get('width') or 0)
        self.height = int(json_vals.get('height') or 0)
        self.orig_delay = json_vals['orig_delay']
        self.delay = float(json_vals['delay'] or 0)
        self.fps = float(json_vals['fps'] or 0)
        self.orig_frame_count = json_vals['orig_frame_count']
        self.orig_frame_count_ds = json_vals['orig_frame_count_ds']
        self.orig_loop_duration = json_vals['orig_loop_duration']
        self.orig_loop_count = int(json_vals['orig_loop_count'] or 0)
        self.loop_count = int(json_vals.get('loop_count') or 0)
        self.rotation = int(json_vals.get('rotation') or 0)
        self.orig_format = json_vals['orig_format']
        self.format = json_vals['format']
        self.skip_frame = json_vals['skip_frame']

        self.flip_x: bool = json_vals.get('flip_x')
        self.flip_y: bool = json_vals.get('flip_y')
        self.is_reversed = json_vals['is_reversed']
        self.preserve_alpha = json_vals['preserve_alpha']

        # self.is_optimized = json_vals['is_optimized']
        # self.optimization_level = json_vals['optimization_level']
        # self.is_lossy = json_vals['is_lossy']
        # self.lossy_value = json_vals['lossy_value']
        # self.is_reduced_color = json_vals['is_reduced_color']
        # self.color_space = json_vals['color_space']
        # self.is_unoptimized = json_vals['is_unoptimized']

        # self.apng_is_optimized = json_vals['apng_is_optimized']
        # self.apng_optimization_level = int(json_vals.get('apng_optimization_level') or 0)
        # self.apng_is_lossy = json_vals['apng_is_lossy']
        # self.apng_lossy_value = int(json_vals.get('apng_lossy_value') or 0)
        # self.apng_is_unoptimized = json_vals['apng_is_unoptimized']

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
        self.create_aimg: CreationCriteria = vals.get('create_aimg')
        self.split_aimg: SplitCriteria = vals.get('split_aimg')
        self.modify_aimg: ModificationCriteria = vals.get('modify_aimg')
        self.build_spr: SpritesheetBuildCriteria = vals.get('build_spr')
        self.slice_spr: SpritesheetSliceCriteria = vals.get('slice_spr')
        self.gif_opt: GIFOptimizationCriteria = vals.get('gif_opt')
        self.apng_opt: APNGOptimizationCriteria = vals.get('apng_opt')
