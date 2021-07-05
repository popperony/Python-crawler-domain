import argparse
from urllib.parse import urlparse
import link
import link_js

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="The URL to extract links from.")
    parser.add_argument("-m", "--max-urls", help="Number of max URLs to crawl, default is 10.", default=5, type=int)

    args = parser.parse_args()
    url = args.url
    max_urls = args.max_urls
    # сбор ссылок с сайта
    all_urls = link.crawl(url, max_urls=max_urls)
    # сбор ссылок с сайта которые используются javascript
    all_urls_js = link_js.crawl(url, max_urls=max_urls)
    # объединение в один массив
    all_urls = all_urls.union(all_urls_js)
    # доменное имя для названия файла
    domain_name = urlparse(url).netloc



    with open(f"output/{domain_name}_links.txt", "w") as f:
        for internal_link in all_urls:
            print(internal_link.strip(), file=f)

    print("[+] General Internal links:", len(link.internal_urls))
    print("[+] General External links:", len(link.external_urls))
    print("[+] Javascript Internal links:", len(link_js.internal_urls_js))
    print("[+] Javascript External links:", len(link_js.external_urls_js))
    print("[+] Total Internal links:", len(link.internal_urls) + len(link_js.internal_urls_js))
    print("[+] Total External links:", len(link.external_urls) + len(link_js.external_urls_js))
    print("[+] Total URLs:", len(link.external_urls) + len(link.internal_urls) + len(link_js.internal_urls_js) + len(link_js.external_urls_js))
    print("[+] Total crawled URLs:", max_urls)