#! /usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import urlunparse
import save


def get_page(url, depth):
    url_parse=urlparse(url)
    Default_Header = {'X-Requested-With': 'XMLHttpRequest',
                      'Referer': url_parse.scheme + '://' + url_parse.netloc,
                      'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36',
                      'Host': url_parse.netloc}
    try:
        page = requests.get(url, headers=Default_Header, verify=True)
    except Exception as reason:
        print("url 打开错误：" + str(reason))
    if page:
        save.save(depth, url, page.content)
        coding = page.encoding
        if coding:
            return page.content


def get_link(url, url_pool, depth):
    new_link = []
    src_url = ""
    href_url = ""
    page_content = get_page(url, depth)

    if page_content == None:
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
        # print("src:  " + str(src))
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
            if src != "" and src_url not in new_link and src_url not in url_pool:
                new_link.append(src_url)

    """
    收集href中的链接
    """
    href_list = soup.findAll(href=re.compile(r"[^\s]+"))
    for href in href_list:
        if re.search("(?<=base)[^>]+", str(href)):
            continue
        # print("href: "+str(href))
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

            if href_url != "" and href_url not in new_link and href_url not in url_pool:
                new_link.append(href_url)
    # print("current url: "+url)
    # print(new_link)
    return new_link


if __name__ == '__main__':
    result = get_link("https://www.github.com", [], 1)
    print(result)
