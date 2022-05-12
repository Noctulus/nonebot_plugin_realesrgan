## 处理图片
import os
from urllib.request import urlretrieve
from basicsr.archs.rrdbnet_arch import RRDBNet
import cv2
from .config import config
# facexlib 和 gfpgan 作为realesrgan的依赖，但是仅用于面部处理，本项目用不到
try:
    from realesrgan import RealESRGANer
except ImportError:
    import pip
    pip.main(['install', '--user', '--no-deps', 'realesrgan'])
    from realesrgan import RealESRGANer

# 两倍放大时所使用的模型
model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=2)
netscale = 2
model_url = "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth"
model_path = "./RealESRGAN_x2plus.pth"
upscaler = RealESRGANer(
    scale=netscale,
    model_path=model_path,
    model=model,
    tile=config.upscale_title_2x,
    tile_pad=0,
    pre_pad=0,
    half=False
)

# 四倍放大时所使用的模型
model_4x = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=6, num_grow_ch=32, scale=4)
netscale_4x = 4
model_4x_url = "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth"
model_4x_path= "./RealESRGAN_x4plus_anime_6B.pth"
upscaler_4x = RealESRGANer(
    scale=netscale_4x,
    model_path=model_4x_path,
    model=model_4x,
    tile=config.upscale_title_4x,
    tile_pad=0,
    pre_pad=0,
    half=False
)

# 放大图片
async def upscale_image(image, output_path: str) -> None:
    if os.path.isfile(model_path) == False:
        urlretrieve(model_url, model_path)
    output, _ = upscaler.enhance(image, outscale=2)
    cv2.imwrite(output_path, output, [cv2.IMWRITE_PNG_COMPRESSION, 6])

async def upscale_image_4x(image, output_path: str) -> None:
    if os.path.isfile(model_4x_path) == False:
        urlretrieve(model_4x_url, model_4x_path)
    output, _ = upscaler_4x.enhance(image, outscale=4)
    cv2.imwrite(output_path, output, [cv2.IMWRITE_PNG_COMPRESSION, 6])