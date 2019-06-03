IMG_EXTS = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff']
STATIC_IMG_EXTS = ['png', 'jpg', 'jpeg', 'bmp']
ANIMATED_IMG_EXTS = ['gif', 'png']


class CreationCriteria():
    """
        Contains all of the GIF/APNG specified criterias like fps, scale, etc.
    """
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
        self.scale: float = 1.0
        self.flip_h: bool = False
        self.flip_v: bool = False
    
    def transform(self, scale, flip_h, flip_v):
        try:
            scale = float(scale)
        except Exception as e:
            raise Exception(e)        
        self.scale = scale
        self.flip_h = flip_h
        self.flip_v = flip_v
        return self
