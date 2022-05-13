import os, random
from urllib.request import urlopen
from typing import List
from nonebot.matcher import Matcher
from nonebot.plugin.on import on_command, on_message
from nonebot.rule import Rule
from nonebot.adapters.onebot.v11 import (
    Bot,
    Message,
    MessageEvent,
    MessageSegment,
    ActionFailed
)
import cv2, numpy

from . import upscale_image
from .config import config

# 一些提示语
_upscale_init_msg="正在放大，请稍候"
_upscale_error_msg="""出现意外错误！可能原因是： 
 - 显存被用完啦！
 - 显卡炸啦！！！"""
_send_error_msg="""图片发送失败！可能原因是：
 - 图片太大啦！
 - 账号被风控啦！"""
_oversize_msg="图片太大了！暂不支持放大"
_gif_msg="暂不支持GIF放大！" # 大概永远也不会支持（
_send_image_msg="放大完毕！正在上传"

# 如果缓存目录不存在则创建目录
os.makedirs(config.upscale_cache_dir, exist_ok=True)

# 响应操作
async def _to_me(bot: Bot, event: MessageEvent) -> bool:
    msgs = event.message
    at_me = bool([i for i in msgs if i.type == "at" and i.data["qq"] == bot.self_id])
    if event.reply:
        has_image = bool([i for i in event.reply.message if i.type == "image"])
    else:
        has_image = bool([i for i in msgs if i.type == "image"])
    return has_image and (event.to_me or at_me)

IMAGE_UPSCALE = on_message(rule=Rule(_to_me), priority=5)
IMAGE_UPSCALE_MODE = on_command("放大", priority=5)

def get_image_urls(msg: Message) -> List[str]:
    return [i.data["url"] for i in msg if i.type == "image" and i.data.get("url")]

# 处理操作
@IMAGE_UPSCALE.handle()
@IMAGE_UPSCALE_MODE.got("IMAGES", prompt="请发送图片")
async def handle_image_upscale(event: MessageEvent) -> None:
    message = event.reply.message if event.reply else event.message
    image_urls = get_image_urls(message)
    if not image_urls:
        await IMAGE_UPSCALE_MODE.reject()    
    filename = str(random.random()) # 使用随机数确保并发处理时不会互相冲突（假装具有并发处理能力）
    output_path = os.path.join(config.upscale_cache_dir,f'{filename}.{config.upscale_output_ext}')
    for i in image_urls:
        try:
            resp = urlopen(i)
            image = cv2.imdecode(numpy.asarray(bytearray(resp.read()), dtype="uint8"), cv2.IMREAD_UNCHANGED)
            image_size = image.shape
            if max(image_size[0], image_size[1]) <=config.upscale_size_max: # 支持从配置中自定义图片大小，以长边为准
                await Matcher.send(_upscale_init_msg)
                try:
                    if max(image_size[0], image_size[1]) <= config.upscale_4x_size_max:
                        await upscale_image.upscale_image_4x(image, output_path)
                    else:
                        await upscale_image.upscale_image(image, output_path)
                    try:
                        await Matcher.send(_send_image_msg)
                        await Matcher.send(message=MessageSegment.image("file:///" + os.path.abspath(output_path)))
                        os.remove(output_path)
                    except ActionFailed: # 发送失败提示
                        await Matcher.send(_send_error_msg)
                except RuntimeError: # 放大失败提示
                    await Matcher.send(_upscale_error_msg)
            else:
                await Matcher.send(_oversize_msg) # 进不去！怎么想都进不去吧
        except AttributeError:
            await Matcher.send(_gif_msg) # GIF 不行