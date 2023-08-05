from aiohttp import ClientSession, FormData

from Findclone import __version__
from .models import Account, Profiles, Histories, get_builder
from .utils import random_string, paint_boxes
from .exceptions import a_error_handler, FindcloneError
from io import BufferedReader, BytesIO


class FindcloneAsync:
    """async findclone api class
    Attributes:
        headers : dict - set requests headers
    """

    def __init__(self):
        self._session = ClientSession()
        self.headers = {"User-Agent": f"findclone-api/{__version__}"}
        self.__builder = get_builder().build_aio_response
        self._session_key = None
        self._userid = None
        self.__info = None

    async def login(self,
                    login: [str, None] = None,
                    password: [str, None] = None,
                    session_key: [str, None] = None,
                    userid: [str, int, None] = None) -> bool:
        """
        *coro
        Findclone authorisation
            :param login: account login
            :param password: account password
            :param session_key: account session_key
            :param userid: account userid
        :return: True is auth success
        """
        if login and password:
            async with self._session.post("https://findclone.ru/login", data={"phone": login,
                                                                              "password": password}) as response:
                await a_error_handler(response)
                resp = await response.json()
                self.__info = await self.__builder(response)
                self._session_key = resp["_session_key"]
                self._userid = resp["_userid"]
                self.headers.update({'session-key': self._session_key, 'user-id': str(self._userid)})
                return True
        elif session_key and userid:
            self.headers.update({"session-key": session_key, "user-id": str(userid)})
            async with self._session.get("https://findclone.ru/profile", headers=self.headers) as response:
                await a_error_handler(response)
                self.__info = await self.__builder(response)
                self._session_key = session_key
                self._userid = userid
                return True
        else:
            raise FindcloneError("Need login and password or session-key and _userid")

    @property
    async def info(self) -> Account:
        """
        *coro
        return account information
        :return: Account object
        """
        async with self._session.get("https://findclone.ru/profile", headers=self.headers) as response:
            info = await self.__builder(response)
            self.__info = info
        return info

    async def upload(self,
                     file: [str, BufferedReader],
                     face_box_id: int = None,
                     timeout: float = 180) -> [Profiles, BytesIO]:
        """
        *coro
        upload image or image url and return Profiles object or BytesIO object
        :param file: image direct download link or path
        :param face_box_id: OPTIONAL, send facebox id if 2 or more faces are detected
        :param timeout: OPTIONAL - max timeout delay
        :return: Profiles object or BytesIO if 2 or more faces are detected
        """
        data = FormData()
        if file.startswith("http"):
            async with self._session.get(file, headers=self.headers) as response:
                file = await response.read()
                data.add_field("uploaded_photo", file, filename=f"{random_string()}.png", content_type="image/png")
        else:
            data.add_field("uploaded_photo", open(file, "rb"), filename=f"{random_string()}.png",
                           content_type="image/png")

        async with self._session.post("https://findclone.ru/upload2", data=data, headers=self.headers,
                                      timeout=timeout) as response:
            resp = await response.json()
            if resp.get("faceBoxes"):
                if face_box_id is not None:
                    async with self._session.get("https://findclone.ru/upload3", params={"id": face_box_id},
                                                 headers=self.headers) as response2:
                        resp = await self.__builder(response2)
                        return resp
                else:
                    img_bytes = paint_boxes(file, resp)  # return bytesIO object
                    return img_bytes
            resp = await self.__builder(response)
            return resp

    async def history(self, offset: int = 0, count: int = 100) -> Histories:
        """
        *coro
        return object histories search for account
        :param offset: int
        :param count: int
        :return: Histories object
        """
        async with self._session.get("https://findclone.ru/hist", params={"offset": offset, "count": count},
                                     headers=self.headers) as response:
            history = await self.__builder(response)
        return history

    async def search(self, search_id: [int, str], count: int = 128) -> Profiles:
        """
        *coro
        :param search_id: [int, str] search id
        :param count: [int] max Profiles count get
        :return: Profiles object
        """
        async with self._session.get("https://findclone.ru/search", params={"id": search_id, "count": count},
                                     headers=self.headers) as response:
            search_result = await self.__builder(response)
        return search_result

    @property
    def get_session(self) -> dict:
        """
        property
        return session-key and _userid account
        :return: dict {"session-key": session_key, "user-id": userid}
        """
        _session = {"session-key": self._session_key, "user-id": self._userid}
        return _session

    def __str__(self):
        return self.__info.__str__()

    async def __aenter__(self) -> 'FindcloneAsync':
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self._session.close()

    async def close(self) -> None:
        await self._session.close()
