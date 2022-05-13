from nonebot import get_driver
from nonebot.config import BaseConfig


class Config(BaseConfig):

    upscale_cache_dir: str = "./cache/"
    upscale_size_max: int = 3000
    upscale_4x_size_max: int = 800
    upscale_title_2x: int = 512
    upscale_title_4x: int = 256
    upscale_output_ext: str = "png"
    upscale_png_compression: int = 6
    upscale_jpg_quality: int = 95

    class Config:
        extra = "ignore"

config = Config(**get_driver().config.dict())