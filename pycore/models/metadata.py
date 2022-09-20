from typing import List, Dict
from dataclasses import dataclass, field
from pycore.utility import filehandler


class ImageMetadata:
    def __init__(self, info):
        self.name = {
            "value": info.get("name"),
            "category": "general_info",
        }
        self.base_filename = {
            "value": info.get("base_filename"),
            "category": "general_info",
        }
        self.width = {
            "value": info.get("width"),
            "category": "general_info",
        }
        self.height = {
            "value": info.get("height"),
            "category": "general_info",
        }
        self.format = {
            "value": info.get("format"),
            "category": "general_info",
        }
        self.format_version = {
            "value": info.get("format_version"),
            # "label": "Full format",
            "category": "general_info",
        }
        self.fsize = {
            "value": info.get("fsize"),
            # "label": "File size (bytes)",
            "category": "general_info",
        }
        self.fsize_hr = {
            "value": filehandler.read_filesize(self.fsize["value"]),
            # "label": "File size",
            "category": "general_info",
        }
        self.absolute_url = {
            "value": info.get("absolute_url"),
            # "label": "Path",
            "category": "general_info",
        }
        self.creation_datetime = {
            "value": info.get("creation_datetime"),
            # "label": "Creation Time",
            "category": "general_info",
        }
        self.modification_datetime = {
            "value": info.get("modification_datetime"),
            # "label": "Modification Time",
            "category": "general_info",
        }
        self.comments = {
            "value": info.get("comments"),
            # "label": "Comments",
            "category": "general_info",
        }
        self.color_mode = {
            "value": info.get("color_mode"),
            "category": "general_info",
        }
        self.color_profile = {
            "value": info.get("color_profile"),
            "category": "general_info",
        }
        self.bit_depth = {
            "value": info.get("bit_depth"),
            "category": "general_info"
        }
        self.has_transparency = {
            "value": info.get("has_transparency"),
            "category": "general_info",
        }
        self.exif = {
            "value": info.get("exif"),
            # "label": "EXIF metadata",
            "category": "general_info",
        }
        self.is_animated = {
            "value": info.get("is_animated"),
            "category": "general_info",
        }
        self.hash_sha1 = {
            "value": info.get("hash_sha1"),
            # "label": "SHA1 Hash",
            "category": "general_info",
        }

    def format_info(self, category_filter=None) -> Dict:
        if category_filter is None:
            category_filter = []
        category_filter = []
        attrs = self.__dict__.items()
        # print(type(attrs))
        categories = {i[1]["category"] for i in attrs}
        if category_filter:
            categories = set(c for c in categories if c in category_filter)
        # print(type(categories))
        info = {}
        for category in categories:
            subinfo = {}
            for k, v in (attr for attr in attrs if attr[1]["category"] == category):
                # print(f"{k} -> {v}")
                # label = v.get("label") or k.replace("_", " ").capitalize()
                subinfo[k] = {
                    "value": v["value"],
                    # "label": label
                }
            info[category] = subinfo
        return info


class AnimatedImageMetadata(ImageMetadata):
    def __init__(self, info):
        self.frame_count = {
            "value": info.get("frame_count"),
            "category": "animation_info",
        }
        self.delays = {
            "value": info.get("delays"),
            # "label": "Delays",
            "category": "animation_info",
        }
        self.delays_are_even = {
            "value": len(set(self.delays["value"])) == 1,
            "category": "animation_info",
        }
        self.average_delay = {
            "value": sum(self.delays["value"]) / len(self.delays["value"]),
            # "label": "Average delay (ms)",
            "category": "animation_info",
        }
        self.fps = {
            "value": round(1000.0 / self.average_delay["value"], 3) if self.average_delay["value"] != 0 else 0,
            # "label": "Frame rate (FPS)",
            "category": "animation_info",
        }
        self.loop_duration = {
            "value": sum(self.delays["value"]) / 1000,
            "category": "animation_info",
        }
        self.loop_count = {
            "value": info.get("loop_count"),
            "category": "animation_info",
        }
        super().__init__(info)
