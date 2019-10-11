from novel.spiders import get_list

if __name__ == '__main__':
    get_list(None, 'http://www.shubao77.vip/0_238/', '#list dl dd a', {'href': {'method': 'attr', 'args': ['href']}, 'title': {'method': 'text', 'args': []}},
             print)
