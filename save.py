#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import re
from urllib.parse import urlparse

page_num = 0


def save(depth, url, page_content):
    global page_num
    depth = str(depth)
    cur_path = os.getcwd()
    # save_file=url.strip().split("/")[-1]
    # save_dir=save_file.split(".")[-1]
    url_parse = urlparse(url)
    save_dir0 = url_parse.netloc
    if url_parse.path.endswith('/') or not url_parse.path:
        save_file = "index_%d.html" % page_num
    else:
        save_file = os.path.basename(url_parse.path)
    save_dir1 = save_file.strip().split(".")[-1]
    no_save = ["doc", "docx", "ppt", "pptx", "pdf", "DOC", "DOCX", "PPT", "PPTX", "PDF"]
    if save_dir1 not in no_save:
        save_dir = os.path.join(cur_path, depth, save_dir0, save_dir1)
        if os.path.isdir(save_dir):
            save_path = os.path.join(save_dir, save_file)
            with open(save_path, "wb") as save_page:
                save_page.write(page_content)
        else:
            os.makedirs(save_dir, exist_ok=True)
    page_num += 1


if __name__ == '__main__':
    save("1", "http://www.scu.edu.cn/jav.js", "3".encode("utf-8"))
