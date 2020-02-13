### Documentation File

# First model

stored = True  **=>** Searchable item 

**Schema**: title=TEXT(stored=True), path=ID(stored=True), content=TEXT, textdata=TEXT(stored=True)

Ranking model: Okapi BM25F

With min bytes value = 100 the pages indexed are 1230


For each query: 
- document (se è solo un nome potrebbe non servire neanche)
- relevance of that document (six level)
- precision (|Ra|/|A|  -> fraction of the retrieved documents, the set A, which is relevant)

^With this values we can find: average precision and NDCG
With the average precision of all queries we can find MAP
