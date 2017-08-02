from pymongo import MongoClient
import jieba
import math
import operator

K1 = 1
B = 0


def bm25(sentence):
    seg_list = jieba.lcut_for_search(sentence)
    n = 0
    word_dict = {}
    for word in seg_list:
        n += 1
        if word in word_dict:
            word_dict[word] += 1
        else:
            word_dict[word] = 1
    scores = {}

    client = MongoClient('localhost', 27017)
    db = client.test
    config_col = db.doc_config
    relation_col = db.relation
    N = 0
    avg_n = 0
    for item in config_col.find():
        N = int(item['N'])
        avg_n = float(item['avg_n'])
    for key in word_dict.keys():
        for item in relation_col.find({"key": key}):
            df = item['number']
            w = math.log2((N - df + 0.5) / (df + 0.5))
            doc_list = item['doc_list']
            docs = str(doc_list).split('\n')
            for doc in docs:
                word = doc.split(', ')
                title = word[0].split('=')[1]
                tf = word[2].split('=')[1]
                if tf is '':
                    tf = 0
                else:
                    tf = int(tf)
                ld = word[3].split('=')[1]
                if ld is '':
                    ld = 0
                else:
                    ld = int(ld)
                s = (K1 * tf * w) / (tf + K1 * (1 - B + B * ld / avg_n))
                if title in scores:
                    scores[title] = scores[title] + s
                else:
                    scores[title] = s
    scores = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
    return scores
