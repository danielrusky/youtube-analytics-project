import json
import os

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        channel = self.get_service().channels().list(id=channel_id, part='snippet,statistics').execute()["items"][0]
        print(channel)
        self.__channel_id = channel_id
        self.title = channel["snippet"]["title"]
        self.url = "https://www.youtube.cpm/channel/" + channel_id
        self.subscriberCount = int(channel["statistics"]["subscriberCount"])
        self.video_count = channel["statistics"]["viewCount"]

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        return self.subscriberCount + other.subscriberCount

    def __sub__(self, other):
        return self.subscriberCount - other.subscriberCount

    def __eq__(self, other):
        return self.subscriberCount == other.subscriberCount

    def __lt__(self, other):
        return self.subscriberCount < other.subscriberCount

    def __le__(self, other):
        return self.subscriberCount <= other.subscriberCount

    def __gt__(self, other):
        return self.subscriberCount > other.subscriberCount

    @property
    def channel_id(self):
        return self.__channel_id

    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('YT_API_KEY')
        return build('youtube', 'v3', developerKey=api_key)

    # def print_info(self) -> None:
    #     Получает данные по API ключу
    #     '''api_key: str = os.getenv('YT_API_KEY')
    #     youtube = build('youtube', 'v3', developerKey=api_key)
    #     dict_to_print = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
    #     print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))
    #     # data_of_channel = dict_to_print['items'][0]'''

    def get_info(self) -> None:
        """Получает данные по API ключу"""
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        dict_to_print = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        data_of_channel = dict_to_print['items'][0]
        self.title = data_of_channel['snippet']['title']
        self.description = data_of_channel['snippet']['description']
        self.url = f"https://www.youtube.com/channel/{self.__channel_id}"
        self.subscriberCount = int(data_of_channel['statistics']['subscriberCount'])
        self.video_count = int(data_of_channel['statistics']['videoCount'])
        self.viewCount = int(data_of_channel['statistics']['viewCount'])

    def to_json(self, file_name):
        data = {"channel_id": self.__channel_id,
                "title": self.title,
                "description": self.description,
                "url": self.url,
                "subscriberCount": self.subscriberCount,
                "video_count": self.video_count,
                "viewCount": self.viewCount}
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        dict_to_print = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))
#