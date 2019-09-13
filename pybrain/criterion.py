class CreationCriteria():
    """ Contains all of the criterias for Creating an animated image """
    def __init__(self, fps, extension, reverse, transparent):
        try:
            fps = float(fps)
        except Exception as e:
            raise Exception(e)
        self.fps: float = fps
        self.duration: float = round(1000 / fps)
        self.extension: str = extension
        self.reverse: bool = reverse
        self.transparent: bool = transparent
        self.flip_h: bool = False
        self.flip_v: bool = False
    
    def transform(self, resize_width, resize_height, flip_h, flip_v):
        try:
            resize_width = float(resize_width)
            resize_height = float(resize_height)
        except Exception as e:
            raise Exception(e)        
        self.resize_width: int = resize_width
        self.resize_height: int = resize_height
        self.flip_h = flip_h
        self.flip_v = flip_v
        return self


class SplitCriteria():
    """ Contains all of the criterias for Splitting an animated image """

    def __init__(self, pad_count, color_space, is_duration_sensitive=False):
        try:
            pad_count = int(pad_count)
            color_space = int(color_space)
        except Exception as e:
            raise Exception(e)
        self.pad_count: int = pad_count
        self.color_space: int = color_space
        self.is_duration_sensitive: bool = is_duration_sensitive


class ModificationCriteria():
    """ Contains all of the criterias for Modifying the specifications of an animated image """

    def __init__(self, json_vals):
        self.orig_width = json_vals['orig_width']
        self.orig_height = json_vals['orig_height']
        self.width = json_vals['width']
        self.height = json_vals['height']
        self.delay = json_vals['delay']
        self.rotation = json_vals['rotation']
        self.fps = json_vals['fps']
        self.format = json_vals['format']
        self.skip_frame = json_vals['skip_frame']

        self.flip_x = json_vals['flip_x']
        self.flip_y = json_vals['flip_y']
        self.is_reversed = json_vals['is_reversed']
        self.preserve_alpha = json_vals['preserve_alpha']

        self.is_optimized = json_vals['is_optimized']
        self.optimization_level = json_vals['optimization_level']
        self.is_lossy = json_vals['is_lossy']
        self.lossy_value = json_vals['lossy_value']
        self.is_reduced_color = json_vals['is_reduced_color']
        self.color_space = json_vals['color_space']

    def must_resize(self):
        return self.orig_width != self.width or self.orig_height != self.height


class SpritesheetBuildCriteria():
    """ Contains all of the criterias to build a spritesheet """

    def __init__(self, resize_width, resize_height, tiles_per_row, offset_x, offset_y, padding_x, padding_y, preserve_alpha):
        self.resize_width: int = int(resize_height)
        self.resize_height: int = int(resize_height)
        self.tiles_per_row: int = int(tiles_per_row)
        self.offset_x: int = int(offset_x)
        self.offset_y: int = int(offset_y)
        self.padding_x: int = int(padding_x)
        self.padding_y: int = int(padding_y)
        self.preserve_alpha: bool = preserve_alpha


class SpritesheetSliceCriteria():
    """ Contains all of the criterias to slice a spritesheet """

    def __init__(self, tile_x, tile_y, offset_x, offset_y, padding_x, padding_y):
        self.tile_x: int = int(tile_x)
        self.tile_y: int = int(tile_y)
        self.offset_x: int = int(offset_x)
        self.offset_y: int = int(offset_y)
        self.padding_x: int = int(padding_x)
        self.padding_y: int = int(padding_y)