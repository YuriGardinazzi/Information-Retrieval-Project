from index_statistics import get_google_ranking
from main import get_title_result
import math

SEPARATOR = ";"

def calculate_statistics():
    dataCSV = "QUERY" + SEPARATOR + "AVERAGE_PRECISION_QUERY" + SEPARATOR + "NDCG\n"
    dict_google_results = get_google_ranking()
    MAP = 0

    for key in dict_google_results:
        average_precision_query = 0
        contRelevant = 0 
        sumRelevance = 0
        relevance = []

        list_titles = get_title_result(key)
        list_titles = [x[:-1] for x in list_titles[0]]

        list_google_titles = [x for x,_ in dict_google_results[key]]
        relevance_google =  [x for _,x in dict_google_results[key]]
 
        for i in range(len(list_titles)):
            if list_titles[i] in list_google_titles:
                contRelevant += 1
                #precision.append(contRelevant / i)
                sumRelevance += (contRelevant / (i + 1))
                relevance.append(relevance_google[list_google_titles.index(list_titles[i])])
            else:
                relevance.append(0)
        if len(list_titles) != 0:
            average_precision_query = sumRelevance / len(list_titles)
        
        # Calcolo DCG e iDCG
        ordered_relevance = relevance.copy()
        ordered_relevance.sort(reverse = True)

        
        j = 2
        DCG = relevance[0]
        iDCG = ordered_relevance[0]
        while j - 1 < len(relevance):
            DCG += relevance[j - 1] / math.log2(j)
            iDCG += ordered_relevance[j - 1] / math.log2(j);
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
