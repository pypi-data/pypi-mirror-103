import nltk
from nltk.tokenize import word_tokenize
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')

from collections import Counter

def extract_noun_counts(doc_list): 
    
    nouns_pdoc = []
    
    for i in range(len(doc_list)):
        pos = nltk.pos_tag(nltk.word_tokenize(doc_list[i]))
        
        print('working on doc ' + str(i+1))
        nouns = []
        for word, pos in pos:
            if pos.startswith('NN'):
                nouns.append(word)
        
        nouns_pdoc.append(nouns)
    
    freq = []

    for nouns in nouns_pdoc:
        freq.append(dict(Counter(nouns)))
        
    return freq


def tfidf(count, count_container):  #'count' in dict type
        
    tfidf = {}
    
    doc_max = 0
    for key, val in count.items():
        if doc_max < val:
            doc_max = val

    all_doc_max = []
    for i in range(len(count_container)):
        temp_max = 0

        for key, val in count_container[i].items():
            if temp_max < val:
                temp_max = val
        all_doc_max.append(temp_max)

    for key, val in count.items():

        idf_sum = 0
        idf = 0
        for i in range(len(count_container)):

            if key in count_container[i].keys():
                idf_sum += count_container[i][key]/all_doc_max[i]
            else:
                idf_sum += 0

        idf = idf_sum/len(count_container) + 1e-10 #'idf' will have a value between 0~1
        tfidf[key] = round((val/doc_max)/idf, 4)

    return Counter(tfidf).most_common()   