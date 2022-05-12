# nonebot_plugin_realesrgan

使用[Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN)进行图片放大的[Nonebot](https://github.com/nonebot/nonebot2)插件

~~刚学 Python 三天，技术力低下（逃~~

## 环境配置

1. 参考[安装 | NoneBot](https://v2.nonebot.dev/docs/start/installation)安装NoneBot和OneBot V11适配器，并参考[创建一个完整的项目 | NoneBot](https://v2.nonebot.dev/docs/tutorial/create-project)创建一个Bot实例；
2. 确保 [PyTorch >= 1.7](https://pytorch.org/) 已安装；
3. 将本插件 `clone` 到插件目录；
4. 运行 `pip install -r requirements.txt` 安装依赖包；
5. 无需提前安装 [realesrgan](https://pypi.org/project/realesrgan/) pip 包；本项目不需要`facexlib`及`gfpgan`（用于面部处理），故采取比较“脏”的方式安装；
6. 在`bot.py`中加载插件`nonebot.load_plugin(nonebot_plugin_realesrgan)`;
7. （可选）在 `.env.*` 中修改配置。

## 触发方式

- 放大模式：
  - 发送 `放大` 会进入放大模式；
  - 此时你发送的下一条消息中如果包含图片，会被放大处理。
- 普通模式：
  - @机器人并发送图片；
  - 回复已发送的图片（可以是别人发送的），并在回复中 @机器人。
- 私聊：
  - 除以上方式外，也可通过直接发送图片触发。

## 配置选项

> 根据自己 GPU 调整合适的配置吧，你也不想让你的显卡走到爆显存吧（  
> 默认配置如下，该配置下使用 RTX 3070 8G 处理一张 1080P 图片约耗时 20 秒，显存占用约 4G。
```
upscale_cache_dir = "./cache/"
upscale_size_max = 3000
upscale_4x_size_max = 800
upscale_title_2x = 512
upscale_title_4x = 256
```
- `upscale_cache_dir` 图片缓存目录，默认`./cache/`；
- `upscale_size_max` 支持放大的图片长边最大值；过大的图片会导致爆显存或生成图片过大无法发送（go-cqhttp最大支持30MB的图片），默认 `3000`；
- `upscale_4x_size_max` 使用四倍放大模式的图片长边最大值；较小图片使用四倍放大而较大图片使用两倍放大，默认 `800`；
- `upscale_title_(2|4)x` 该值越大则处理越快，同时显存占用越高。
  
## TODO

- [ ] 使用 Poetry 打包及发布
- [ ] 上传至 Nonebot 商店
- [ ] 支持分群开启
- [ ] 增加指令CD
- [x] 咕咕咕~