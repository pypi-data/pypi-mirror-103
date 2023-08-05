from requests import Response
from aiohttp import ClientResponse


class FindcloneError(Exception):
    pass


def error_handler(response: Response):
    """error handler for sync findclone class"""
    if response.status_code != 200:
        if isinstance(response.json(), dict):
            if response.json().get("Error"):
                raise FindcloneError(f"error_code: {response.status_code}", response.json()["Error"])
    return True


async def a_error_handler(response: ClientResponse):
    """error handler for async findclone class"""
    resp = await response.json()
    if response.status != 200:
        if isinstance(resp, dict):
            if resp.get("Error"):
                raise FindcloneError(f"error_code: {response.status}", resp["Error"])

    return True

