from pycore.utility import  filehandler


class ImageMetadata:
    def __init__(self, info):
        self.name = {
            "value": info.get("name"),
            "label": "Name",
            "category": "general_info",
        }
        self.base_filename = {
            "value": info.get("base_filename"),
            "label": "Base filename",
            "category": "general_info",
        }
        self.width = {
            "value": info.get("width"),
            "label": "Width",
            "category": "general_info",
        }
        self.height = {
            "value": info.get("height"),
            "label": "Height",
            "category": "general_info",
        }
        self.format = {
            "value": info.get("format"),
            "label": "Format",
            "category": "general_info",
        }
        self.format_version = {
            "value": info.get("format_version"),
            "label": "Full format",
            "category": "general_info",
        }
        self.fsize = {
            "value": info.get("fsize"),
            "label": "File size (bytes)",
            "category": "general_info",
        }
        self.fsize_hr = {
            "value": filehandler.read_filesize(self.fsize["value"]),
            "label": "File size",
            "category": "general_info",
        }
        self.absolute_url = {
            "value": info.get("absolute_url"),
            "label": "Path",
            "category": "general_info",
        }
        self.creation_datetime = {
            "value": info.get("creation_datetime"),
            "label": "Creation Time",
            "category": "general_info",
        } 
        self.modification_datetime = {
            "value": info.get("creation_datetime"),
            "label": "Modification Time",
            "category": "general_info",
        } 
        self.comments = {
            "value": info.get("comments"),
            "label": "Comments",
            "category": "general_info",
        }
        self.color_mode = {
            "value": info.get("color_mode"),
            "label": "Color mode",
            "category": "general_info",
        }
        self.transparency = {
            "value": info.get("transparency"),
            "label": "Transparency info",
            "category": "general_info",
        }
        self.exif = {
            "value": info.get("exif"),
            "label": "EXIF metadata",
            "category": "general_info",
        }
        self.is_animated = {
            "value": info.get("is_animated"),
            "label": "Is animated",
            "category": "general_info",
        }
        self.hash_sha1 = {
            "value": info.get("hash_sha1"),
            "label": "SHA1 Hash",
            "category": "general_info",
        }

    def format_info(self):
        attrs = self.__dict__.items()
        # print(type(attrs))
        categories = {i[1]["category"] for i in attrs}
        # print(type(categories))
        info = {}
        for category in categories:
            subinfo = {}
            for k, v in (attr for attr in attrs if attr[1]["category"] == category):
                # print(f"{k} -> {v}")
                subinfo[k] = {"value": v["value"], "label": v["label"]}
            info[category] = subinfo
        return info


class AnimatedImageMetadata(ImageMetadata):
    def __init__(self, info):
        self.frame_count = {
            "value": info.get("frame_count"),
            "label": "Frame count",
            "category": "animation_info",
        }
        self.delays = {
            "value": info.get("delays"),
            "label": "Delays",
            "category": "animation_info",
        }
        self.delays_are_even = {
            "value": len(set(self.delays["value"])) == 1,
            "label": "Delays are even",
            "category": "animation_info",
        }
        self.average_delay = {
            "value": sum(self.delays["value"]) / len(self.delays["value"]),
            "label": "Average delay (ms)",
            "category": "animation_info",
        }
        self.fps = {
            "value": round(1000.0 / self.average_delay["value"], 3) if self.average_delay["value"] != 0 else 0,
            "label": "FPS",
            "category": "animation_info",
        }
        self.loop_duration = {
            "value": sum(self.delays["value"]) / 1000,
            "label": "Loop duration",
            "category": "animation_info",
        }
        self.loop_count = {
            "value": info.get("loop_count"),
            "label": "Loop count",
            "category": "animation_info",
        }
        super().__init__(info)
