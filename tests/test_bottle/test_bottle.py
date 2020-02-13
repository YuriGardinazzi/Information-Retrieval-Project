# -*- coding: utf-8 -*-
"""
Hello world of a webpage made with bottle
"""

from bottle import route, run, template

@route('/')
def index():
    return '<h1>Hello WORLD!</h1>'

run(host='localhost', port=8080)