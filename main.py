import argparse
from urllib.parse import urlparse

import link
# import link_js

# # внутренние ссылки - на страницы внутри сайта
# internal_urls = set()
# # внешние ссылки - на другие сайты
# external_urls = set()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Link Extractor Tool with Python")
    parser.add_argument("url", help="The URL to extract links from.")
    parser.add_argument("-m", "--max-urls", help="Number of max URLs to crawl, default is 10.", default=10, type=int)

    args = parser.parse_args()
    url = args.url
    max_urls = args.max_urls
    # сбор ссылок с сайта
    all_urls = link.crawl(url, max_urls=max_urls)
    # сбор ссылок с сайта которые используются javascript
    # all_urls_js = link_js.crawl(url, max_urls=max_urls)
    # объединение в один массив
    # all_urls = all_urls.union(all_urls_js)
    # доменное имя для названия файла
    domain_name = urlparse(url).netloc



    with open(f"output/{domain_name}_links.txt", "w") as f:
        for internal_link in all_urls:
            print(internal_link.strip(), file=f)

    print("[+] Total Internal links:", len(internal_urls))
    print("[+] Total External links:", len(external_urls))
    print("[+] Total URLs:", len(external_urls) + len(internal_urls))
    print("[+] Total crawled URLs:", max_urls)