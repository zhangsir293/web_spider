import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import urlunparse


def get_link(url,url_pool):
    new_link = []
    try:
        page = requests.get(url)
    except Exception as reason:
        print("url 打开错误："+str(reason))
    if not page:
        return []
    page_content = page.content
    coding = page.encoding
    if not coding:
        return []
    """
    解析页面
    """
    soup = BeautifulSoup(page_content, 'html.parser')
    """
    解析url地址
    """
    url_parse = urlparse(url)
    """
    收集src中的链接
    """
    src_list = soup.find_all(src=re.compile(r"[^\s]+"))
    for src in src_list:
        #print("src:  " + str(src))
        src_str = re.search("src=(\"|\')?(?P<src>[^\"\']+)", str(src))
        if src_str:
            src_link = src_str.groupdict()["src"]
            src_parse = urlparse(src_link)
            if not src_parse.netloc:
                data = [url_parse.scheme, url_parse.netloc,
                        src_parse.path, src_parse.params,
                        src_parse.query, src_parse.fragment]
                src_url = urlunparse(data)
            elif src_parse.netloc == url_parse.netloc:
                src_url = src_link
            if src_url not in new_link and src_url not in url_pool:
                new_link.append(src_url)

    """
    收集href中的链接
    """
    href_list = soup.findAll(href=re.compile(r"[^\s]+"))
    for href in href_list:
        if re.search("(?<=base)[^>]+", str(href)):
            continue
        #print("href: "+str(href))
        href_re = re.search("href=(\"|\')?(?P<href>[^\"\']+)", str(href))
        if href_re:
            href_link = href_str = href_re.groupdict()["href"]
            href_parse = urlparse(href_str)
            if not href_parse.netloc:
                href_data = [url_parse.scheme, url_parse.netloc,
                             href_parse.path, href_parse.params,
                             href_parse.query, href_parse.fragment]
                href_url = urlunparse(href_data)
            elif href_parse.netloc == url_parse.netloc:
                href_url = href_link

            if href_url not in new_link and href_url not in url_pool:
                new_link.append(href_url)

    # print("current url: "+url)
    # print(new_link)
    return new_link


if __name__ == '__main__':
    get_link("http://www.scu.edu.cn/portal2013/inc/appvar.js")

