from typing import Optional

from nonebot import get_driver
from pydantic import Extra, BaseModel, AnyHttpUrl, Field


class Config(BaseModel, extra=Extra.ignore):
    smms_api_url: AnyHttpUrl = Field(default="https://sm.ms/api/v2")
    smms_token: Optional[str] = None


plugin_config = Config(**get_driver().config.dict())
