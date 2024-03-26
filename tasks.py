from celery_app import app
import requests
import xmltodict
from utils import get_print_form_links, retry_request


class FetchLinksTask(app.Task):
    name = 'fetch_links_task'

    def run(self, page_number):
        print(f'Fetching links from page {page_number}...')
        links = get_print_form_links(page_number)
        for link in links:
            parse_xml.delay(link)


@app.task(bind=True, base=FetchLinksTask)
def fetch_links(self, page_number):
    return self.run(page_number)


class ParseXmlTask(app.Task):
    name = 'parse_xml_task'

    def run(self, url):
        print(f'Parsing XML for {url}...')
        response = retry_request(url)
        if response is not None:
            print(response, url)
            data = xmltodict.parse(response.content)
            first_key = next(iter(data))
            publish_date = data[first_key].get('commonInfo', {}).get('publishDTInEIS', None)
            print(f'{url} - {publish_date}')
        else:
            print(f"Не удалось получить данные для {url}")


@app.task(bind=True, base=ParseXmlTask)
def parse_xml(self, url):
    return self.run(url)
