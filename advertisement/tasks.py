from celery import shared_task
from advertisement.crawler.jobinja_crawler import JobinjaLinkCrawler, JobinjaDataCrawler


@shared_task
def crawl_jobinja():
    JobinjaDataCrawler().start()
