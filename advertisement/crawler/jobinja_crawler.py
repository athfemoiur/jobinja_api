from bs4 import BeautifulSoup
from django.db import transaction

from advertisement.crawler.utils import BaseCrawler
from advertisement.models import CrawlerConfig, Link, Company, Advertisement, Tag, TagValue
from .config import HEADER
from threading import Thread
from queue import Queue


class JobinjaLinkCrawler(BaseCrawler):
    def __init__(self):
        self.config = CrawlerConfig.objects.filter(source=CrawlerConfig.JOBINJA).first()
        self.base_url = self.config.url
        self.queue = self.create_queue()

    @staticmethod
    def get_advertisements_link(html_doc):
        soup = BeautifulSoup(html_doc, 'html.parser')
        return [lnk.get('href') for lnk in soup.find_all('a', attrs={'class': 'c-jobListView__titleLink'})]

    def create_queue(self):
        url = self.base_url + "&page={}"
        queue = Queue()
        for i in range(1, 21):
            queue.put(url.format(i))
        return queue

    def crawl(self):
        while True:
            #  using python queue and multithreading
            url = self.queue.get()
            response = self.get(url, header=HEADER)
            if response:
                links = self.get_advertisements_link(response.text)
                self.store(links)
                self.queue.task_done()
            else:
                self.queue.put(url)
            if self.queue.empty():
                break

    def start(self):
        #  multithreading
        for _ in range(6):
            thread = Thread(target=self.crawl)
            thread.start()
        self.queue.join()

    @staticmethod
    def store(links):
        link_objects = [Link(url=link, source=Link.JOBINJA) for link in links]
        Link.objects.bulk_create(link_objects)


class Parser:

    def parse_all_data(self, html_doc):
        soup = BeautifulSoup(html_doc, 'html.parser')

        adv_data = {
            'title': self.parse_title(soup),
            'description': self.parse_description(soup),
            'company_name': self.parse_company_name(soup),
            'company_description': self.parse_company_desc(soup),
            'remaining_days': self.parse_days_remaining(soup),
        }

        adv_data.update(self.parse_tags(soup))
        return adv_data

    @staticmethod
    def parse_title(soup):
        data = soup.find('div', {'class': 'c-jobView__titleText'})
        if data is not None:
            data = data.string
        return data

    @staticmethod
    def parse_description(soup):
        data = ""
        tag = soup.find('div', {'class': 's-jobDesc'})
        if tag is not None:
            for string in tag.stripped_strings:
                data += string
        return data

    @staticmethod
    def parse_company_name(soup):
        data = ""
        tag = soup.find('h2', {'class': 'c-companyHeader__name'})
        if tag is not None:
            for string in tag.stripped_strings:
                data += string
        return data

    @staticmethod
    def parse_company_desc(soup):
        data = ""
        tag = soup.select_one(
            '#singleJob > div > div:nth-child(1) > div.col-md-8.col-sm-12.js-fixedWidgetSide > section > '
            'div:nth-child(6)')
        if tag is not None:
            for string in tag.stripped_strings:
                data += string
        return data

    @staticmethod
    def parse_days_remaining(soup):
        data = ""
        tag = soup.find('p', {'class': 'u-textCenter'})
        if tag is not None:
            for string in tag.stripped_strings:
                data += string
        return data

    @staticmethod
    def parse_tags(soup):
        # returns a dict of tags(length is unknown)
        data = dict()

        key_tags = [h4.text for h4 in soup.find_all('h4', {'class': 'c-infoBox__itemTitle'})]
        value_tags = soup.find_all('div', {'class': 'tags'})

        for key, value in zip(key_tags, value_tags):
            contents = list(value.stripped_strings)
            data[key] = [contents[0].replace("\n", "")] if len(contents) == 1 else contents

        return data


class JobinjaDataCrawler(BaseCrawler):

    def __init__(self):
        self.links = Link.objects.filter(source=Link.JOBINJA, crawled=False)
        self.queue = self.create_queue()
        self.parser = Parser()

    def crawl(self):
        while True:
            url_object = self.queue.get()
            url = url_object.url
            response = self.get(url, header=HEADER)
            if response:
                data = self.parser.parse_all_data(response.text)
                self.store(url, data)
                self.update_crawled_flag(url_object)
                self.queue.task_done()
            else:
                self.queue.put(url_object)

            if self.queue.empty():
                break

    def create_queue(self):
        queue = Queue()
        for link in self.links:
            queue.put(link)
        return queue

    def start(self):
        for _ in range(10):
            thread = Thread(target=self.crawl)
            thread.start()
        self.queue.join()

    @staticmethod
    def update_crawled_flag(link_object):
        link_object.crawled = True
        link_object.save()

    def store(self, url, data):
        with transaction.atomic():
            company, _ = Company.objects.get_or_create(title=data.get('company_name'),
                                                       description=data.get('description'))
            advertisement = Advertisement.objects.create(source=Advertisement.JOBINJA, url=url, title=data.get('title'),
                                                         description=data.get('description'), company=company,
                                                         remaining_days=data.get('remaining_days'))
            for key, value in list(data.items())[5:]:
                tag, _ = Tag.objects.get_or_create(title=key)
                TagValue.objects.create(tag=tag, advertisement=advertisement, value=value)
