<!-- markdownlint-disable MD033 MD036 MD041-->
<div align="center">

# nonebot-plugin-smms

_✨ sm.ms 图床插件 ✨_

</div>

<p align="center">
  <a href="https://raw.githubusercontent.com/mobyw/nonebot-plugin-smms/master/LICENSE">
    <img src="https://img.shields.io/github/license/mobyw/nonebot-plugin-smms.svg" alt="license">
  </a>
  <a href="https://pypi.python.org/pypi/nonebot-plugin-smms">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-smms.svg" alt="pypi">
  </a>
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">
</p>

## 简介

本插件提供 [sm.ms](https://sm.ms/) 图床的上传、删除、查询上传历史功能。

## 安装

### 使用 `nb-cli` 安装（推荐）

```bash
nb plugin install nonebot-plugin-smms
```

### 使用 `pip` 安装

```bash
pip install nonebot-plugin-smms
```

需要在 bot 根目录 `pyproject.toml` 文件中 [tool.nonebot] 部分添加：

```python
plugins = ["nonebot_plugin_smms"]
```

## Driver 设置

需要参考 [driver](https://nonebot.dev/docs/appendices/config#driver) 配置项，添加 `HTTPClient` 支持（如 `~httpx`），在对应 env 文件（如 `.env` `.env.prod`）中，根据所用适配器的要求进行如下配置：

```text
DRIVER=~fastapi+~httpx
```

```text
DRIVER=~httpx+~websockets
```

## 插件环境配置

在对应 env 文件（如 `.env` `.env.prod`）中，可以设置如下参数。

sm.ms API token:

```text
SMMS_API_URL="https://smms.app/api/v2"
```

替换默认 sm.ms API 地址（https://sm.ms/api/v2）:

```text
SMMS_TOKEN="your_token"
```

## 使用说明

如需在其他插件中使用上传图片等功能，可以从本插件导入。

导入方式：

```python
from nonebot import require
require("nonebot_plugin_smms")
from nonebot_plugin_smms import SMMS
```

基本使用方式（以 QQ 适配器为例）：

```python
smms = SMMS()
image = ... # bytes, BytesIO, Path
file = await smms.upload(image)
if file:
    await matcher.send(MessageSegment.image(file.url))
    await smms.delete(file.hash)
    await matcher.finish("图片上传并删除成功")
else:
    await matcher.finish("图片上传失败")
```
