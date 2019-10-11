# !/usr/bin/env python3
# -*- coding:utf-8 -*-


import json
from .websocket_server import WebsocketServer
from novel.setting import server


class Server(WebsocketServer):
    callMethod = {}

    def __init__(self):
        super(Server, self).__init__(server['port'], server['ip'])
        self.set_fn_new_client(self.new_client)
        self.set_fn_message_received(self.get_message)
        self.run_forever()

    def new_client(self, client, servers: WebsocketServer):
        servers.send_message(client, json.dumps({"status": "0", "type": "msg", "msg": "连接成功", "data": {}}))

    def get_message(self, client, servers, message):
        """
        获得客户端的信息
        :param client:
        :param WebsocketServer servers:
        :param message:
        :return:
        """
        try:
            data = json.loads(message)
        except ValueError as e:
            data = {}
            pass
        if 'type' in data:
            if data['type'] == "cmd":
                data = getattr(self, data['cmd'])(*data['args'])
                if data is None:
                    pass
                else:
                    servers.send_message(client, json.dumps(data))
        else:
            servers.send_message(client, json.dumps({"status": "10001", "type": "msg", "msg": "口令错误", "data": {}}))

    def stop(self):
        self.server_close()

    def start(self, data):
        pass
