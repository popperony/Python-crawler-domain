import argparse
from urllib.parse import urlparse

import parser_link
import parser_link_js


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="The URL to extract links from.")
    parser.add_argument("-m", "--max-urls", help="Number of max URLs to crawl, default is 10.", default=5, type=int)  # NOQA E501

    args = parser.parse_args()
    url = args.url
    max_urls = args.max_urls
    # сбор ссылок с сайта
    all_urls = parser_link.crawl(url, max_urls=max_urls)
    # сбор ссылок с сайта которые используются javascript
    all_urls_js = parser_link_js.crawl(url, max_urls=max_urls)
    # объединение в один массив
    all_urls = all_urls.union(all_urls_js)
    # доменное имя для названия файла
    domain_name = urlparse(url).netloc

    with open(f"output/{domain_name}_links.txt", "w", encoding='utf-8') as file:  # NOQA E501
        for i in all_urls:
            print(i.strip(), file=file)

    # print("[+] General Internal links:", len(parser_link.internal_urls))
    # print("[+] General External links:", len(parser_link.external_urls))
    # print("[+] Javascript Internal links:", len(parser_link_js.internal_urls_js))  # NOQA E501
    # print("[+] Javascript External links:", len(parser_link_js.external_urls_js))  # NOQA E501
    print("[+] Total Internal links:", len(parser_link.internal_urls) + len(parser_link_js.internal_urls_js))  # NOQA E501
    print("[+] Total External links:", len(parser_link.external_urls) + len(parser_link_js.external_urls_js))  # NOQA E501
    print("[+] Total URLs:", len(parser_link.external_urls) + len(parser_link.internal_urls) + len(parser_link_js.internal_urls_js) + len(parser_link_js.external_urls_js))  # NOQA E501
    print("[+] Total crawled URLs:", max_urls)
