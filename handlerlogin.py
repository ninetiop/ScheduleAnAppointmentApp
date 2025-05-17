#!/usr/bin/env python3

import logging
import tornado.web
import handler
import json


class HandlerLogin(handler.Handler):
    def __init__(self, application, request, **kwargs ):
        super(handler.Handler, self).__init__(application, request, **kwargs)
        self._init_log()
        return

    def initialize(self, static_path, path, db):
        super(handler.Handler, self).initialize()
        self._static_path = static_path
        self._path = path
        self._db = db
        return

    def _init_log(self):
        self.__log = logging.getLogger(__name__)
        return

    @tornado.gen.coroutine
    def get(self):
        self.__log.info('Get Index')
        self.render(self._static_path + '/' + self._path,
                static_path=self._static_path+'/')
        return
    
    @tornado.gen.coroutine
    def post(self):
        ret = None
        json_obj = json.loads(json.loads(self.request.body))
        username = json_obj['username']
        password = json_obj['password']
        auth = self._db.login(username, password)
        if auth :
            self.set_secure_cookie("user", username)
            #self.redirect("/admin")
            ret = {
                'success': True
            }
            self.set_header("Content-Type", "application/json")
            self.write(json.dumps(ret))
            self.finish()
        else:
            # Authentication failed, show an error message or redirect back to the login page
            ret = {
                'success': False
            }
            self.set_header("Content-Type", "application/json")
            self.write(json.dumps(ret))
            self.finish()
        """
        else:
            ret = {
                'success': False
            }
            self.set_header("Content-Type", "application/json")
            self.write(json.dumps(ret))
            self.finish()
        """


