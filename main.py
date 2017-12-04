import spider
from concurrent.futures import ThreadPoolExecutor

def main():
    url_tree = {}
    url_pool = ["http://www.scu.edu.cn", ]
    deep = 3

    for depth in range(deep):
        url_tree[depth] = []
        if depth == 0:
            new_task = url_pool.copy()
        else:
            new_task = url_tree[depth-1].copy()
        with ThreadPoolExecutor(3) as executor:
            for each in new_task:
                new_link=executor.submit(spider.get_link,each,url_pool)
                url_tree[depth].extend(new_link.result())
                url_pool.extend(new_link.result())
        # for each in new_task:
        #     print(str(depth)+": "+str(each))
        #     new_link = spider.get_link(each, url_pool)
        #     url_tree[depth].extend(new_link)
        #     url_pool.extend(new_link)

        print(depth)
        print(url_tree[depth])
        # for each in url_tree[depth]:
        #     print(each)



if __name__ == '__main__':
    main()
