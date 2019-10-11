server = {
    'port': '8003',
    'ip': '0.0.0.0',
}

test_data = [{
    'method': 'page_handle',
    'args': {
        "url": "http://www.shubao77.vip/xiaoshuo_7/",
        "next_page": "#pagelink > a.next",
        "encoding": "gbk",
        "callback": {
            "get_list": {
                "list_css": "#newscontent > div.l > ul > li > span.s2 > a",
                "items_css": {
                    "title": {"method": "text", "args": []},
                    "href": {"method": "attr", "args": ['href']}
                },
                "callback": {
                    "list_handle": {
                        "callback": {
                            "print": {
                                # "list_css": "#list > dl > dd > a",
                                # "items_css": {"href": {"method": "attr", "args": ['href']}},
                                # "callback": {
                                #     "list_handle": {
                                #         "callback": {
                                #             "get_data": {
                                #                 "items_css": {
                                #                     "title": {"css": "#wrapper > div.content_read > div > div.bookname > h1", "method": "text", "args": []},
                                #                     "content": {"css": "#content", "method": "text", "args": []},
                                #                 },
                                #                 "encoding": "gbk",
                                #                 "callback": {"print": {}},
                                #             }
                                #         }
                                #     }
                                # },
                            }
                        }
                    }
                },
                "encoding": "gbk"
            }
        }
    }
}]
# newscontent > div.l > ul > li:nth-child(1) > span.s2 > a
