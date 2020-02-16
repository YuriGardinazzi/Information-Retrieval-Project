from whoosh.fields import Schema, TEXT, NGRAM, ID
from whoosh.index import create_in
from dump_splitter import PagesHandler
from index_creator import Index
from whoosh.index import open_dir
from whoosh.highlight import HtmlFormatter
from whoosh.qparser import MultifieldParser, OrGroup
from whoosh.qparser.plugins import FuzzyTermPlugin, PlusMinusPlugin
from whoosh.index import open_dir
from whoosh.qparser import QueryParser

#schema = Schema(title=TEXT(stored=True), content=TEXT(stored=True), titleAuto=NGRAM(3, 4), id=ID(stored=True))


def create_index_suggestion():
    ix = Index("index", "pages")
    ix.setSchemaSuggestion()
    ix.createIndex()
#In index creator
#def setSchemaSuggestion(self):
 #       self.schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True), textdata	=NGRAM(3, 4))

def get_suggestion(q):
    ix = open_dir('index')

    with ix.searcher() as searcher: # Un searcher apre diversi file, quindi va preferibilmente usato con il with in modo da farli anche chiudere
        og = OrGroup.factory(0.9) # Dalla documentazione ufficiale, maggiore priorità se ci sono più termini
        parser = MultifieldParser(['title', 'content'], ix.schema, {'title': 1.0, 'content': 0.2}, group=og) # Dai priorità ai titoli
        parser.add_plugin(PlusMinusPlugin()) # Consente di specificare con + e - termini che ci devono essere o no
        parser.add_plugin(FuzzyTermPlugin()) # Consente di cercare termini non precisi con la tilde (~)
        # parser.add_plugin(ForceFuzzyPlugin()) # Un mio hack, vedi dopo

        query = parser.parse(q)
        #print(query) # Per fare debug

        results = searcher.search(query)
        results.formatter = HtmlFormatter(between=' &hellip; ') # Questioni di gusto

        # Simulazione della stampa dei risultati in un terminale, anziché usare HTML e un template engine
        for r in results:
            titleHigh = r.highlights("title")
            title = titleHigh if titleHigh else r['title'] # Se non c'è il termine nel titolo, senza questa linea non verrebbe stampato nulla
            #print(title, 'n', r.highlights("content"), 'n')

    parser = QueryParser('textdata', ix.schema) # Cerchiamo solo in textdata
    query = parser.parse(q)
    
    list_results = []
    with ix.searcher() as searcher:
        results = searcher.search(query)

        for r in results[0:10]:
            #print(r['title'])
            list_results.append(r['title'][:-1])

    return list_results

if __name__ == "__main__":
    create_index_suggestion()
    print(get_suggestion("maya"))
