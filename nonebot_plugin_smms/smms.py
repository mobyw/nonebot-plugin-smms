import asyncio
from io import BytesIO
from http import HTTPStatus
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from pydantic import ValidationError

from nonebot import get_driver
from nonebot.log import logger
from nonebot.drivers import HTTPClientMixin, Request

from .config import plugin_config
from .model import ApiResponse, FileInfo


class SMMS:
    driver: HTTPClientMixin
    headers: Dict[str, Any]

    def __init__(self):
        driver = get_driver()
        if not isinstance(driver, HTTPClientMixin):
            raise RuntimeError(
                f"Current driver {driver.config.dict()} does not support "
                "http client requests! "
                "sm.ms plugin requires HTTPClient driver."
            )
        if plugin_config.smms_token is None:
            raise RuntimeError("No sm.ms token is set!")
        self.driver = driver
        self.headers = {"Authorization": plugin_config.smms_token}

    async def upload(self, file: Union[bytes, Path, BytesIO]) -> Optional[FileInfo]:
        """
        Upload image to sm.ms.
        """
        if isinstance(file, Path):
            smfile = file.read_bytes()
        elif isinstance(file, BytesIO):
            smfile = file.getvalue()
        else:
            smfile = bytes(file)
        request = Request(
            "POST",
            url=f"{plugin_config.smms_api_url}/upload",
            headers=self.headers,
            files={"smfile": smfile},
            timeout=60,
        )
        logger.debug("sm.ms upload begin...")
        response = await self.driver.request(request)
        logger.debug(
            f"sm.ms upload response: {response.status_code} {response.content}"
        )
        if response.status_code != HTTPStatus.OK or response.content is None:
            logger.error(
                f"sm.ms upload failed with status code: {response.status_code}"
            )
            return None
        try:
            content = ApiResponse.parse_raw(response.content)
        except ValidationError as e:
            logger.error(f"sm.ms upload response validation error: {e}")
            return None
        if not content.success or not isinstance(content.data, FileInfo):
            logger.error(f"sm.ms upload failed: {content.message}")
            return None
        return content.data

    async def delete(self, hash: str):
        """
        Delete image from sm.ms.
        """
        request = Request(
            "GET",
            url=f"{plugin_config.smms_api_url}/delete/{hash}",
            headers=self.headers,
            timeout=60,
        )
        logger.debug("sm.ms delete begin...")
        response = await self.driver.request(request)
        logger.debug(
            f"sm.ms delete response: {response.status_code} {response.content}"
        )
        if response.status_code != HTTPStatus.OK or response.content is None:
            logger.error(
                f"sm.ms delete failed with status code: {response.status_code}"
            )
            return False
        try:
            content = ApiResponse.parse_raw(response.content)
        except ValidationError as e:
            logger.error(f"sm.ms delete response validation error: {e}")
            return False
        if not content.success:
            logger.error(f"sm.ms delete failed: {content.message}")
            return False
        return True

    async def upload_history(self) -> List[FileInfo]:
        """
        Get image upload history from sm.ms.
        """
        request = Request(
            "GET",
            url=f"{plugin_config.smms_api_url}/upload_history",
            headers=self.headers,
            timeout=60,
        )
        logger.debug("sm.ms get upload history begin...")
        response = await self.driver.request(request)
        logger.debug(
            f"sm.ms get upload history response: {response.status_code} {response.content}"
        )
        if response.status_code != HTTPStatus.OK or response.content is None:
            logger.error(
                f"sm.ms get upload history failed with status code: {response.status_code}"
            )
            return []
        try:
            content = ApiResponse.parse_raw(response.content)
        except ValidationError as e:
            logger.error(f"sm.ms history response validation error: {e}")
            return []
        if not content.success or not isinstance(content.data, list):
            logger.error(f"sm.ms history failed: {content.message}")
            return []
        return content.data
