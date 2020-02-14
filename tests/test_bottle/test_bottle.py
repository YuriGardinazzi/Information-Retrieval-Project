# -*- coding: utf-8 -*-
"""
Hello world of a webpage made with bottle
"""

from bottle import route, run, error

@route('/')
def index():
    return '<h1>Hello WORLD!</h1>'

@error(404)
def error404(error):
    return 'Nothing here, sorry'

if __name__ == "__main__":
  
    run(host='localhost', port=8080)