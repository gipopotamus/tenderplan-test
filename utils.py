import time

import requests
import xmltodict
from bs4 import BeautifulSoup
from requests import HTTPError


def retry_request(url, max_retries=10, delay=2):
    """
    Пытается выполнить HTTP GET-запрос к указанному URL максимально заданное количество раз (`max_retries`),
    делая паузу (`delay` в секундах) между попытками.
    :param url: URL для запроса
    :param max_retries: Максимальное количество попыток
    :param delay: Задержка между попытками
    """
    for attempt in range(max_retries):
        try:
            cookies = {
                'doNotAdviseToChangeLocationWhenIosReject': 'true',
                '_ym_uid': '1711469429509169520',
                '_ym_d': '1711469429',
                '_ym_isad': '1',
                '_ym_visorc': 'b',
            }
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Language': 'ru,en;q=0.9',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Upgrade-Insecure-Requests': '1',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
            }
            response = requests.get(url, headers=headers, cookies=cookies)
            response.raise_for_status()
            return response
        except HTTPError as e:
            print(f"Попытка {attempt + 1} из {max_retries}. HTTP ошибка: {e}, URL: {url}")
        time.sleep(delay)

    print(f"Не удалось выполнить запрос после {max_retries} попыток, URL: {url}")
    return None  # Все попытки неудачны


def get_print_form_links(page_number):
    url = f'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?fz44=on&pageNumber={page_number}'
    response = retry_request(url)
    print(response)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = []
    for entry in soup.find_all("div", class_="search-registry-entry-block box-shadow-search-input"):
        print_link = entry.find("a", href=True, target="_blank")
        if print_link and 'printForm/view.html' in print_link['href']:
            full_link = f"https://zakupki.gov.ru{print_link['href'].replace('view.html', 'viewXml.html')}"
            links.append(full_link)
    return links


