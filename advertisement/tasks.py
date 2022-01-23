from celery import shared_task
from advertisement.crawler.jobinja_crawler import JobinjaLinkCrawler, JobinjaDataCrawler


@shared_task
def crawl_jobinja():
    JobinjaLinkCrawler().start()
    print('link crawl finished')
    JobinjaDataCrawler().start()
    print('data crawl finished')
    return '*** task crawl_jobinja done ***'
