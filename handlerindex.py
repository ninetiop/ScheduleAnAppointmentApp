#!/usr/bin/env python3

import logging
import tornado.web
import handler
import json

from scheduler import Scheduler

class HandlerIndex(handler.Handler):
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
        if not 'slot' in json_obj.keys():
            row_appointments = self._db.get_appointments(json_obj['date'])
            scheduler = Scheduler(row_appointments)
            available_slot = scheduler.get_full_day_available_slot(json_obj['date'])
            formatted_slots = [slot.strftime('%Y-%m-%d %H:%M:%S') for slot in available_slot]
            ret = {
                'success': True,
                'slots': formatted_slots
            }
            self.set_header("Content-Type", "application/json")
            self.write(json.dumps(ret))
            self.finish()
        else:
            appointment_slot = json_obj['date'] + ' ' + json_obj['slot'] + ':00'
            row_to_insert = {
                "firstname": json_obj['prenom'],
                "lastname": json_obj['nom'],
                "date": appointment_slot[:-3]
            }
            self._db._insert_appointment(row_to_insert)
            ret = {
                'success': True
            }
            self.set_header("Content-Type", "application/json")
            self.write(json.dumps(ret))
            self.finish()
