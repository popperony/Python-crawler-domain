import requests
from urllib.request import urlparse, urljoin
from bs4 import BeautifulSoup
import colorama

# определяем цвета для внешних и внутренних ссылок
colorama.init()
GREEN = colorama.Fore.GREEN
BLUE = colorama.Fore.BLUE
RED = colorama.Fore.RED
RESET = colorama.Fore.RESET

# множество для сбора только уникальных ссылок
all_urls = set()

total_urls_visited = 0
# внутренние ссылки - на страницы внутри сайта
internal_urls = set()
# внешние ссылки - на другие сайты
external_urls = set()

# проверяем в url правильную схему и домен
def is_valid(url):
    parsed = urlparse(url)
    if bool(parsed.netloc) and bool(parsed.scheme):
        return True
    return False


def get_all_website_links(url):
    """
    Возвращает все найденные URL на текущем сайте
    """
    urls = set()
    # доменное имя без указания протокола
    domain_name = urlparse(url).netloc
    try:
        global soup
        soup = BeautifulSoup(requests.get(url).content, "html.parser", from_encoding="iso-8859-1")
    except Exception as exc:
        print(f'{RED} {exc} {RESET}')

    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # если в тэге нет ссылки
            continue
        # присоединям к URL домен если ссылка относительная
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # очищаем URL от лишних параметров
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid(href):
            # если не валидна ссылка идем к след
            continue
        if href in all_urls:
            # если есть уже в наборе
            continue
        if domain_name not in href:
            # если домена нет в ссылке, значит она внешняя
            if urlparse(href).netloc not in all_urls:
                # печатаем серым цветом и сохраняем в набор (наше множество)
                print(f"{BLUE}[!] External link: {href}{RESET}")
                all_urls.add(href)
                external_urls.add(href)
            continue
        urls.add(href)
        if parsed_href.netloc not in all_urls:
            print(f"{GREEN}[*] Internal link: {href}{RESET}")
            all_urls.add(href)
            internal_urls.add(href)
    return urls

        

def crawl(url, max_urls=5):
    """
    Сканирвание страницы, извлечение всех ссылок.
    Все ссылки складываются в наборы external_urls и internal_urls
    max_urls - максимальное количество ссылок для сканирования, по умолчанию 5
    """
    global total_urls_visited
    total_urls_visited += 1
    links = get_all_website_links(url)
    for link in links:
        if total_urls_visited > max_urls:
            break
        crawl(link, max_urls=max_urls)
    return all_urls

