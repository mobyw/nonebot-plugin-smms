from nonebot import get_driver
from nonebot.log import logger
from nonebot.drivers import HTTPClientMixin
from nonebot.plugin import PluginMetadata

from .config import Config, plugin_config

__plugin_meta__ = PluginMetadata(
    name="sm.ms图床",
    description="sm.ms图床上传与管理",
    usage="参考项目 README",
    type="library",
    config=Config,
    homepage="https://github.com/mobyw/nonebot-plugin-smms",
    supported_adapters=None,
)

driver = get_driver()


@driver.on_startup
async def on_startup():
    if not isinstance(driver, HTTPClientMixin):
        logger.error(
            f"Current driver {driver.config.dict()} does not support "
            "http client requests! "
            "sm.ms plugin requires HTTPClient driver."
        )
    if plugin_config.smms_token is None:
        logger.warning("No sm.ms token is set!")


from .smms import SMMS as SMMS
from .model import FileInfo as FileInfo
