from typing import List
from datetime import datetime

from requests import Response as _Response
from aiohttp import ClientResponse
from .Exceptions import a_error_handler, error_handler


class Account:
    """
    Account information object
    Attributes:
        raw_data : dict return raw dict response
        quantity : int - return quantity requests
        period : int - return period subscription in seconds
        typename : str - return subscription type
        userid : int - return findclone _userid
        period_days : int - period subscription in days
    """
    def __init__(self):
        self.raw_data: [dict, None] = None  # full json response
        self.quantity: [int, None] = None  # count requests
        self.period: [int, None] = None  # seconds of subscription
        self.typename: [str, None] = None  # type subscription
        self.userid: [int, None] = None  # findclone account id

    def __str__(self):
        """
        :return: string information
        quantity, period_days, type
        """
        return f"quantity: {self.quantity} period: {self.period_days} type: {self.typename}"

    @property
    def period_days(self) -> int:
        """convert seconds to day
        :return: int"""
        return int(round(self.period / 60 / 60 / 24, 0)) - 1


class History:
    """History object
    Attributes:
        raw_data : dict - return raw response
        date : int - return date request to unix time
        id : int - return search request id
        thumbnail : str -  return thumbnail to base64"""
    def __init__(self):
        self.raw_data: [dict, None] = None
        self.date: [int, str, None] = None
        self.id: [int, None] = None
        self.thumbnail: [str, None] = None

    def unix_to_date(self, format_time='%Y-%m-%d %H:%M:%S'):
        """
        format unix time to date
        :param format_time: strftime string
        :type format_time: str
        :return: datetime
        """
        return datetime.utcfromtimestamp(int(self.date)).strftime(format_time)

    def __str__(self):
        """
        :return: date search and id
        """
        return f"date: {self.unix_to_date()} id: {self.id}"


class Histories:
    """Histories object
    Attributes:
        raw_histories : list - return raw response history
    """
    def __init__(self):
        self.raw_data: [List[dict], None] = None
        self.__history_list: List[History] = list()

    def _prettify(self) -> None:
        for _history in self.raw_data:
            history = History()
            history.raw_data = _history
            history.date = _history["date"]
            history.id = _history["id"]
            history.thumbnail = _history["thumbnail"]
            self.__history_list.append(history)

    def __iter__(self) -> iter(List[History]):
        """
        return list of History objects
        :return: list[History]
        """
        return iter(self.__history_list)


class Detail:
    """Detail object
    Attributes:
        photoid : int - return photoid
        size : int - return size face detect
        url : str - return url image
        userid : int - return vk _userid
        (x,y) : (int, int) - return coords detected face"""
    def __init__(self):
        self.raw_data: [list, None] = None
        self.photoid: [int, None] = None
        self.size: [int, None] = None
        self.url: [str, None] = None
        self.userid: [int, None] = None
        self.x: [int, None] = None
        self.y: [int, None] = None

    def __str__(self):
        return f"{self.url_source} {self.url}"

    @property
    def url_source(self) -> str:
        """
        :return: vk.com path url
        """
        return f"https://vk.com/photo{self.userid}_{self.photoid}"


class Profile:
    """Profile object
    Attributes:
        profile: dict - return raw response
        age : [str, None] - return age if different else return None
        city : [str, None] - return city if different else return None
        raw_details : list - return list of dict sources photos
        details : list - return list of object Detail
        firstname : str - return first name
        score : float - return match result score
        url : str - return vk.com url
        """

    def __init__(self):
        self.profile: [dict, None] = None
        self.age: [int, None] = None
        self.city: [str, None] = None
        self.raw_data: [List[dict], None] = None
        self.raw_details: [list, None] = None
        self.details: List[Detail] = list()
        self.firstname: [str, None] = None
        self.score: [float, None] = None
        self.url: [str, None] = None

    def _prettify(self) -> None:
        for _detail in self.raw_details:
            detail = Detail()

            detail.raw_data = _detail
            detail.photoid = _detail["photoid"]
            detail.size = _detail["size"]
            detail.url = _detail["url"]
            detail.userid = _detail["_userid"]
            detail.x = _detail["x"]
            detail.y = _detail["y"]
            self.details.append(detail)

    def __iter__(self) -> iter(List[Detail]):
        """
        return iter list of Detail objects
        :return: iter(List[Detail])
        """
        return iter(self.details)

    def __str__(self):
        """
        :return: string formatted info
        """
        return f"{self.url} {self.score} {self.firstname} {self.city} {self.age}"


class Profiles:
    """
    Attributes:
        raw_profiles : list - return raw response
        total : int - return profiles count
        thumbnail : str - return base64 encode image
    """
    def __init__(self):
        self.raw_data: [list, None] = None
        self.total: [int, None] = None
        self.thumbnail: [str, None] = None
        self.__profiles_list: List[Profile] = list()

    def _prettify(self) -> None:
        for _profile in self.raw_data:
            profile = Profile()
            age = _profile.get("Age")
            city = _profile.get("city")
            details = _profile["details"]
            firstname = _profile["firstname"]
            score = _profile["score"]
            url = "https://vk.com/id" + str(_profile['_userid'])

            profile.raw_data = _profile
            profile.profile = _profile
            profile.age = age
            profile.city = city
            profile.raw_details = details
            profile.firstname = firstname
            profile.score = score
            profile.url = url
            profile._prettify()
            self.__profiles_list.append(profile)

    def __iter__(self) -> iter(List[Profile]):
        """
        return list of Profile objects
        :return: iter(List[Profiles])
        """
        return iter(self.__profiles_list)


def get_builder(): return _Builder()


class _Builder:
    """
    Class builder objects
    """

    @staticmethod
    def build_response(response: [_Response]) -> [Account, Histories, Profiles]:
        error_handler(response)
        resp_url = response.url.split("?")[0]
        # Build account information object
        if resp_url.endswith("profile"):
            account = Account()
            response = response.json()
            account.raw_data = response
            account.quantity = response["Quantity"]
            account.period = response["Period"]
            account.typename = response["TypeName"]
            account.userid = response["_userid"]
            return account
        # Build histories search object
        elif resp_url.endswith("hist"):
            histories = Histories()
            response = response.json()
            histories.raw_data = response
            histories._prettify()
            return histories
        # Build profiles object
        elif resp_url.endswith("upload2") or resp_url.endswith("upload3") or resp_url.endswith("upload") \
                or resp_url.endswith("search"):
            profiles = Profiles()
            response = response.json()
            profiles.raw_data = response["data"]
            profiles.total = response["Total"]
            profiles._prettify()
            return profiles

    @staticmethod
    async def build_aio_response(response: ClientResponse) -> [Account, Histories, Profiles]:
        await a_error_handler(response)
        resp_url = str(response.url).split("?")[0]
        # Build account information object
        if resp_url.endswith("profile"):
            account = Account()
            response = await response.json()
            account.raw_data = response
            account.quantity = response["Quantity"]
            account.period = response["Period"]
            account.typename = response["TypeName"]
            account.userid = response["_userid"]
            return account
        # Build histories search object
        elif resp_url.endswith("hist"):
            histories = Histories()
            response = await response.json()
            histories.raw_data = response
            histories._prettify()
            return histories
        # Build profiles object
        elif resp_url.endswith("upload2") or resp_url.endswith("upload3") or resp_url.endswith("upload") \
                or resp_url.endswith("search"):
            profiles = Profiles()
            response = await response.json()
            profiles.raw_data = response["data"]
            profiles.total = response["Total"]
            profiles._prettify()
            return profiles
