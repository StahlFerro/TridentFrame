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
        self.fps = fps
        self.duration = round(1000 / fps)
        self.extension = extension
        self.reverse = reverse
        self.transparent = transparent
        self.scale = 1.0
        self.flip_h = False
        self.flip_v = False
    
    def transform(self, scale, flip_h, flip_v):
        try:
            scale = float(scale)
        except Exception as e:
            raise Exception(e)        
        self.scale = scale
        self.flip_h = flip_h
        self.flip_v = flip_v
        return self
