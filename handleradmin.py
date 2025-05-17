#!/usr/bin/env python3
import json
import logging
import tornado.web
import handler
import datetime

from scheduler import DELTA_SHIFT_BETWEEN_APPOINTMENT

class HandlerAdmin(handler.Handler):
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
        cookie_header = self.request.headers.get("Cookie")
        cookie_secret = self.application.settings.get("cookie_secret")
        if not cookie_secret or not cookie_header:
            self.set_status(401)  # Set status code to 400 Bad Request
            self.finish("Not authorized")  # Return an error message or response
            return
        
        if self.application.settings.get("cookie_secret"):    
            self.__log.info('Get Admin.html')
            data = []
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            rows_appointments = self._db.get_appointments(current_date)
            for row in rows_appointments:
                obj = {
                'firstname': row[1],
                'lastname': row[2],
                'date': str(row[3]).split(' ')[1][:-3]
                }
                data.append(obj)
            self.render(self._static_path + '/' + self._path,
                    static_path=self._static_path+'/', data = data)
            return

    @tornado.gen.coroutine
    def post(self):
        ret = None
        data = []
        json_obj = json.loads(json.loads(self.request.body))
        if json_obj['action'] == 'get_appointment':
            date = json_obj['date']
            date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
            formatted_date = date_obj.strftime("%Y-%m-%d")
            rows_appointments = self._db.get_appointments(formatted_date)
            for row in rows_appointments:
                obj = {
                'firstname': row[1],
                'lastname': row[2],
                'date': str(row[3]).split(' ')[1][:-3]
                }
                data.append(obj)
            ret = {
                'success': True,
                'appointments': data
            }
        if json_obj['action'] == 'archiver':
            date = json_obj['date']
            ret = self._db.update_status(json_obj)
            ret = {
                'success': ret
            }
        if json_obj['action'] == 'supprimer':
            date = json_obj['date']
            ret = self._db.delete_row(json_obj)
            ret = {
                'success': ret
            }
            
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(ret))
        self.finish()





