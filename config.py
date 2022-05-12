from nonebot import get_driver
from nonebot.config import BaseConfig


class Config(BaseConfig):

    upscale_cache_dir = "./cache/"
    upscale_size_max = 3000
    upscale_4x_size_max = 800
    upscale_title_2x = 512
    upscale_title_4x = 256

    class Config:
        extra = "ignore"

config = Config(**get_driver().config.dict())