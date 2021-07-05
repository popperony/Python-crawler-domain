import requests
from requests_html import HTMLSession
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import re
import link
import colorama
from seleniumwire import webdriver
import codecs


colorama.init()
GREEN = colorama.Fore.GREEN
BLUE = colorama.Fore.BLUE
RED = colorama.Fore.RED
RESET = colorama.Fore.RESET

all_urls = set()
all_links = set()
urls = set()

total_urls_visited_js = 0
# внутренние ссылки - на страницы внутри сайта
internal_urls_js = set()
# внешние ссылки - на другие сайты
external_urls_js = set()

regexp = r"https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/;=]*)"

# проверяем в url правильную схему и домен
def is_valid(url):
    parsed = urlparse(url)
    if bool(parsed.netloc) and bool(parsed.scheme):
        return True
    return False

def chek_url(href,domain_name):

    parsed_href = urlparse(href)
    href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
    if not is_valid(href):
        return None
    if href in all_urls:
        return None
    if domain_name not in href:
        if urlparse(href).netloc not in all_urls:
            print(f"{BLUE}[!] External link: {urlparse(href).netloc}{RESET}")
            all_urls.add(urlparse(href).netloc)
            external_urls_js.add(urlparse(href).netloc)
        return None
    if href[-3:] != 'jpg' and href[-3:] != 'css' and href[-3:] != 'png' and href[-3:] != 'ttf' and href[-3:] != 'gif':
        urls.add(href)
    if parsed_href.netloc not in all_urls:
        print(f"{GREEN}[*] Internal link: {parsed_href.netloc}{RESET}")
        all_urls.add(parsed_href.netloc)
        external_urls_js.add(parsed_href.netloc)

def get_all_website_links(url):
    domain_name = urlparse(url).netloc
    firefoxdriver = r'./drivers/geckodriver'
    options2 = webdriver.FirefoxOptions()
    options2.headless = True
    # options2 = webdriver.ChromeOptions()
    options2.add_argument('headless')
    options = {
            'disable_encoding': True
        }
    # driver = webdriver.Chrome(chrome_options=options2,seleniumwire_options=options)
    driver = webdriver.Firefox(executable_path=firefoxdriver, options=options2, seleniumwire_options=options)

    # response = session.get(url)
    driver.get(url)
    # извлекаем js
    for request in driver.requests:
        if request.response:
            if request.url == url:
                try:
                    regex = regexp
                    all = re.findall(regex, request.response.body.decode('utf-8'))
                    for al in all:
                        chek_url(al,domain_name)
                except Exception as exc:
                    print(f'{RED} {exc} {RESET}')
            href = request.url
            chek_url(href,domain_name)
    driver.quit()
    return urls.copy()


def crawl(url, max_urls=5):
    global total_urls_visited_js
    global all_links
    global urls
    total_urls_visited_js += 1
    links = get_all_website_links(url)

    for link in links:
        if total_urls_visited_js > max_urls:
            break
        if link not in all_links and (link[:4] == 'http' or link[:5] == 'https'):
            all_links.add(link)
            crawl(link, max_urls=max_urls)
    return all_urls
