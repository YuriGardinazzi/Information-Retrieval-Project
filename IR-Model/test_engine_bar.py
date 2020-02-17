# -*- coding: utf-8 -*-
"""
Hello world of a webpage made with bottle
"""

from bottle import route, run, error, request, get, post
from main import get_retrieved_pages, getSuggestion, get_did_you_mean, get_expanded_terms
from bottle import template
variable = ["er", "e"]
SEARCH_BAR = '''
        <form action="/search" method="post">
            <input list="suggestion" oninput="setSuggestion()" type="text" id="query" name="query" placeholder="Search..." value="{{value}}">
                  <datalist id="suggestion">   
                               
                  </datalist>
            <input type="submit" id="input" name="search" value="Search">
        </form>
        <script>
            function setSuggestion()
            {
                console.log("SON DENTRO")
                
                
                var options = '';
                var xhttp = new XMLHttpRequest();
                xhttp.onreadystatechange = function() {
                    if (this.readyState == 4 && this.status == 200) {
                       // Typical action to be performed when the document is ready:
                      console.log(xhttp.responseText);
                      result = xhttp.responseText;
                      var obj = JSON.parse(result);
                     
                      num = obj.num    //num field from json answer
                      list = obj.list; //list field from json answer
                      var i;
                      var vet = new Array(num);
                      for(i = 0; i < num; i++){
                             vet[i] = list[i]
                      }
                      
                      var options = ""
                      //add retrieved value to datalist element in html
                      for(var i = 0; i < vet.length; i++)
                          options += '<option value="'+ vet[i] +'" />';

                      document.getElementById('suggestion').innerHTML = options;
                    }
                };
                filename ="get_sugg/"+document.getElementById("query").value
                xhttp.open("GET", filename, true);
                xhttp.send();

                
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

@route('/get_sugg/<value>')
def test_char(value):
    print("INPUT:  ",value)
    sugg = getSuggestion(value)
    ris ={ "num": len(sugg)}
    if len(ris) != 0:
        ris["list"] = sugg

    return ris
@get('/search')
def search():
    return template(SEARCH_BAR, value="")

@post('/search')
def do_research():
    query = request.forms.get('query')
    
    text = SEARCH_BAR

    text += '<form"><pre>'
    
    didyoumean = get_did_you_mean(query)
    expanded = get_expanded_terms(didyoumean[1])
    if len(expanded) > 0:
        print("EXPANDED: ", expanded)
        text += '<h4> added terms: '+ expanded + '</h4>'


    pages = get_retrieved_pages(query)
    
    #print("Len Titoli: ", len(data_title), "Len testo: ", len(data_text))
    #for title , page in data_title, data_text:
    if pages != None:
        if didyoumean[0]:
            text +=  '<h4> Results for: ' + didyoumean[1] + '</h4>'
        for page in pages:
            link = get_wiki_link(page[0])
            text += '<a href="' + link +'""> ' + page[0] + '</a>'
            text += '<p> ' + page[1] + '</p>'
        if len(expanded) > 0:
            exp_pages = get_retrieved_pages(expanded)
            if (exp_pages):
                for page in exp_pages:
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

@error(500)
def error500(error):
    print(error)
    return search()
@error(404)
def error404(error):
    return 'Nothing here, sorry'

if __name__ == "__main__":
  
    run(host='localhost', port=8080)
