# -*- coding: utf-8 -*-
"""
Hello world of a webpage made with bottle
"""

from bottle import route, run, error, request, get, post
from main import get_retrieved_pages
from bottle import template
variable = ["er", "e"]
SEARCH_BAR = '''
        <form action="/search" method="post">
            <input list="suggestion" onkeypress="setSuggestion()" type="text" id="query" name="query" placeholder="Search..." value="{{value}}">
                  <datalist id="suggestion">   
                               
                  </datalist>
            <input type="submit" name="search" value="Search">
        </form>
        <script>
            function setSuggestion()
            {
                var ar = new Array();
                ar[0]='val1';
                ar[1]='val';
                ar[1]='val hei';

                var options = '';

                for(var i = 0; i < ar.length; i++)
                  options += '<option value="'+ ar[i] +'" />';

                document.getElementById('suggestion').innerHTML = options;
            }
        </script>
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
    return template(SEARCH_BAR, value="")

@post('/search')
def do_research():
    query = request.forms.get('query')
    
    text = SEARCH_BAR

    text += '<form"><pre>'
    pages = get_retrieved_pages(query)
    
    #print("Len Titoli: ", len(data_title), "Len testo: ", len(data_text))
    #for title , page in data_title, data_text:
    if pages != None:
      
        for page in pages:
            link = get_wiki_link(page[0])
            text += '<a href="' + link +'""> ' + page[0] + '</a>'
            text += '<p> ' + page[1] + '</p>'
    else:
        text += '<h3> NO RESULTS </h3>'
    text += '</pre></form>'
    return template(text, value = query)

@route('/')
def index():
    return search()

@error(404)
def error404(error):
    return 'Nothing here, sorry'

if __name__ == "__main__":
  
    run(host='localhost', port=8080)
