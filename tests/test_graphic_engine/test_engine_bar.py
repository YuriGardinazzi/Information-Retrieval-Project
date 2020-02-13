# -*- coding: utf-8 -*-
"""
Hello world of a webpage made with bottle
"""

from bottle import route, run, error, request, get, post
from main import get_title_result

SEARCH_BAR = '''
        <form action="/search" method="post">
            <input type="text" id="query" name="query" placeholder="Search...">
            <input type="submit" name="search" value="Search">
        </form>  
    '''

def get_wiki_link(el):
    link = "https://en.wikipedia.org/wiki/"
    for c in el:
        if c != ' ':
            link += c
        else:
            link += '_'

    return link

@get('/search')
def search():
    return SEARCH_BAR

@post('/search')
def do_research():
    query = request.forms.get('query')
    
    text = SEARCH_BAR

    text += '<form"><pre>'
    data_title, data_text = get_title_result(query)
    for i in range(len(data_title)):
        link = get_wiki_link(data_title[i])
        text += '<a href="' + link +'""> ' + data_title[i] + '</a>'
        text += '<p> ' + data_text[i] + '</p>'
    text += '</pre></form>'
    return text

@route('/')
def index():
    return search()

@error(404)
def error404(error):
    return 'Nothing here, sorry'

if __name__ == "__main__":
  
    run(host='localhost', port=8080)
