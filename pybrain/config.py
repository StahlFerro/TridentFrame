IMG_EXTS = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff']
STATIC_IMG_EXTS = ['png', 'jpg', 'jpeg', 'bmp']
ANIMATED_IMG_EXTS = ['gif', 'png']


class CreationCriteria():
    """ Contains all of the criterias for Creating an animated image """
    def __init__(self, fps, extension, reverse, transparent):
        try:
            fps = float(fps)
        except Exception as e:
            raise Exception(e)
        self.fps: int = fps
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
        self.resize_width = resize_width
        self.resize_height = resize_height
        self.flip_h = flip_h
        self.flip_v = flip_v
        return self


class SplitCriteria():
    """ Contains all of the criterias for Splitting an animated image """

    def __init__(self, pad_count, is_duration_sensitive=False):
        self.pad_count: int = pad_count
        self.is_duration_sensitive: bool = is_duration_sensitive
