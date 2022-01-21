from abc import ABC, abstractmethod
import requests


class BaseCrawler(ABC):

    @staticmethod
    def get(url, header=None):
        try:
            response = requests.get(url, headers=header)
        except requests.HTTPError:
            print('unable to get response and there is no status code')
            return None
        if response.status_code == 200:
            return response
        print(f'unable to get response, status code : {response.status_code}')
        return None

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def crawl(self):
        pass

    @abstractmethod
    def store(self, *args, **kwargs):
        pass
