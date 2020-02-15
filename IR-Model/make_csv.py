from index_statistics import get_google_ranking
from main import get_retrieved_pages
import math

SEPARATOR = ";"

def calculate_statistics():
    dataCSV = "QUERY" + SEPARATOR + "AVERAGE_PRECISION_QUERY" + SEPARATOR + "NDCG\n"
    dict_google_results = get_google_ranking()
    MAP = 0

    for key in dict_google_results.keys():
        average_precision_query = 0
        contRelevant = 0 
        sumRelevance = 0
        relevance = []

        r_pages = get_retrieved_pages(key) #list of tuples (title, text_page)
        list_titles = [x[0] for x in r_pages] #retrieved titles
        
        google_title_and_relevance = dict_google_results[key] #list of tuples (title,relevance)
        list_google_titles = [x[0] for x in dict_google_results[key]] #google retrieved titles
        relevance_google =  [x[1] for x in dict_google_results[key]] #google retrieved relevance
 
        #print("KEY: ", key,"\nLIST:",list_google_titles, end ="\n\n")
        for t in list_titles:
            #t[:-1] to remove \n at the end of the tiltes
            if t[:-1] in list_google_titles:
                contRelevant += 1
                #precision.append(contRelevant / i)
                pos = list_google_titles.index(t[:-1])
               # print(pos)
                sumRelevance += (contRelevant / (pos + 1))
                relevance.append(relevance_google[pos])
                #relevance.append(relevance_google[list_google_titles.index(list_titles[i])])
            else:
                relevance.append(0)
        if len(list_google_titles) != 0:
            average_precision_query = sumRelevance / len(list_google_titles)
        
        # Calcolo DCG e iDCG
        ordered_relevance = relevance.copy()
        ordered_relevance.sort(reverse = True)

        
        j = 2
        DCG = relevance[0]
        iDCG = ordered_relevance[0]
        while j - 1 < len(relevance):
            DCG += relevance[j - 1] / math.log2(j)
            iDCG += ordered_relevance[j - 1] / math.log2(j)
            j += 1

        NDCG = 0
        if iDCG != 0:
            NDCG = DCG / iDCG

        dataCSV += key + SEPARATOR + str(average_precision_query) + SEPARATOR + str(NDCG) + '\n'
        MAP += average_precision_query
        
    MAP /= len(dict_google_results)
    dataCSV += '\n\n'
    dataCSV += "MAP" + SEPARATOR + str(MAP) + '\n'
    with open("statistics.csv", 'w', encoding='utf-8') as f:
        f.write(dataCSV)

if __name__ == "__main__":
    calculate_statistics()
