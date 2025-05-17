#!/usr/bin/env python3

import logging
import os
import secrets
import tornado.web
import tornado.ioloop
import tornado.httpserver

from tornado.options import options
from handlerindex import HandlerIndex
from handlerlogin import HandlerLogin
from handleradmin import HandlerAdmin
from databasemanager import DatabaseManager
from configparse import ConfigParse


cookie_secret = secrets.token_hex(32)

class Server:

    def __init__(self, port=5454):
        self._config = ConfigParse()
        self._init_log()
        self._init_db()
        self._port = port
        settings = {
                'debug': True,
                'static_path': os.path.join(os.path.dirname(__file__), 'static'),
                }

        static_path = os.path.join(os.path.dirname(__file__), 'static')
        self._app = tornado.web.Application([
            (r"/", HandlerIndex, {
                    'static_path':'static',
                    'path':'index.html',
                    'db': self._db
                }
            ),
            (r"/login", HandlerLogin, {
                'static_path':'static',
                    'path':'login.html',
                    'db': self._db
                }
            ),
            (r"/admin", HandlerAdmin, {
                'static_path':'static',
                    'path':'admin.html',
                    'db': self._db
                }
            ),
            (r"/static/(.*)", tornado.web.StaticFileHandler,
                {
                    'path': settings['static_path'],
                    
                    }
            )
        ],  cookie_secret=cookie_secret)

        return

    def _init_db(self):
        config = self._config.get_config()
        self._db = DatabaseManager(config['host'],
                                   config['port'],
                                   config['name'],
                                   config['user'],
                                   config['password']
                                   )
        self._db._create_connection()

    def _init_log(self):
        self.__log = logging.getLogger('tornado.access')
        return

    def run(self):
        self.__log.info('Listen on port {}'.format(self._port))
        print('Listen on port {}'.format(self._port))
        self._app.listen(self._port)
        tornado.ioloop.IOLoop.current().start()
        return

    def stop(self):
        self._ioloop.stop()
        return

def main():
    server = Server()
    server.run()

if __name__ == '__main__':
    main()

main()