import requests
from pyquery import PyQuery as PQ
from urllib.parse import urlparse
from os.path import dirname, exists, join
from os import makedirs
from time import sleep


class Spiders:
    session_pool = {}
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    }

    def get_session(self, url) -> requests.session:
        url_info = urlparse(url)
        if url_info.netloc not in self.session_pool:
            self.session_pool[url_info.netloc] = requests.session()
            self.session_pool[url_info.netloc].headers.update(self.header)
        return self.session_pool[url_info.netloc]

    def get_list(self, data, list_css: str, items_css, callback, encoding="utf-8", ):
        if isinstance(data, PQ):
            pq = data
        else:
            if isinstance(data, dict):
                data = data['href']
            while True:
                res = self.get_session(data).get(data)
                if res.status_code == 200:
                    res.encoding = encoding
                    pq = PQ(res.text)
                    pq.make_links_absolute(base_url=data)
                    break
                sleep(3)
        items = pq(list_css).items()
        result = []
        for item in items:
            tmp = {}
            for x, y in items_css.items():
                tmp[x] = getattr(item, y['method'])(*y['args'])
            result.append(tmp)
        for method, args in callback.items():
            getattr(self, method)(result, **args)

    def get_data(self, data, items_css, callback, encoding="utf-8"):
        if isinstance(data, PQ):
            pq = data
        else:
            if isinstance(data, dict):
                data = data['href']
            while True:
                res = self.get_session(data).get(data)
                if res.status_code == 200:
                    res.encoding = encoding
                    pq = PQ(res.text)
                    pq.make_links_absolute(base_url=data)
                    break
                sleep(3)
        result = {}
        for x, y in items_css.items():
            result[x] = getattr(pq(y['css']), y['method'])(*y['args'])
        for method, args in callback.items():
            getattr(self, method)(result, **args)

    @staticmethod
    def down_img(src: str, path='.'):
        res = requests.get(src)
        url_info = urlparse(src)
        if res.status_code == 200:
            filename = join(path, url_info.path[1:])
            if not exists(dirname(filename)):
                makedirs(dirname(filename))
            with open(filename, 'wb') as fp:
                fp.write(res.content)
        else:
            return False

    @staticmethod
    def down_text(src: str, path=''):
        res = requests.get(src)
        url_info = urlparse(src)
        if res.status_code == 200:
            filename = join(path, url_info.path)
            if not exists(dirname(filename)):
                makedirs(dirname(filename))
            with open(filename, 'w') as fp:
                fp.write(res.text)
        else:
            return False

    def list_handle(self, data, callback):
        for item in data:
            for method, args in callback.items():
                getattr(self, method)(item, **args)

    def page_handle(self, data, url='', next_page='', callback={}, encoding='utf-8'):
        while True:
            res = self.get_session(url).get(url)
            res.encoding = encoding
            if res.status_code == 200:
                pq = PQ(res.text)
                pq.make_links_absolute(url)
                for method, args in callback.items():
                    getattr(self, method)(pq, **args)
                if pq(next_page).length > 0:
                    url = pq(next_page).attr('href')
                else:
                    break
            else:
                print(res.status_code)
                with open('ff.html', 'wb') as fp:
                    fp.write(res.content)
            sleep(2)

    def print(self, res):
        print(res)

    def task(self, data):
        result = []
        for item in data:
            result = getattr(self, item['method'])(result, **item['args'])
