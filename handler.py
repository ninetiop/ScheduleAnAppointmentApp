#!/usr/bin/env python3
from typing import Any

import tornado.web
import tornado.gen
from tornado.web import Application


class Handler(tornado.web.RequestHandler):
    def __init__(self, application: Application, request, **kwargs: Any) -> None:
        super().__init__(application, request, **kwargs)
