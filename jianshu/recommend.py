import jieba.analyse
import pandas as pd
import numpy as np
from sklearn.metrics import pairwise_distances
from pymongo import MongoClient


def get_dt_matrix(files, topK = 200):
    M = files.count()
    N = 1
    keys = {}
    dt = []
    for file in files:
        title = file['title']
        content = file['content']
        tags = jieba.analyse.extract_tags(title + '。' + content, topK=topK, withWeight=True)
        word_dict = {}
        for word, tfidf in tags:
            word_dict[word] = tfidf
            if word not in keys:
                keys[word] = N
                N += 1
        dt.append([title, word_dict])
    dt_matrix = [[0 for i in range(N)] for j in range(M)]
    i = 0
    for title, t_tfidf in dt:
        dt_matrix[i][0] = title
        for key, tfidf in t_tfidf.items():
            dt_matrix[i][keys[key]] = tfidf
        i += 1
    dt_metrix = pd.DataFrame(dt_matrix)
    dt_metrix.index = dt_metrix[0]
    return dt_metrix


def get_k_matrix(dt_matrix, k):
    k_nearest = []
    tmp = np.array(1 - pairwise_distances(dt_matrix[dt_matrix.columns[1:]], metric='cosine'))
    similarity_matrix = pd.DataFrame(tmp, index=dt_matrix.index.tolist(), columns=dt_matrix.index.tolist())
    for i in similarity_matrix.index:
        tmp = [i, []]
        j = 0
        while j < k:
            max_col = similarity_matrix.loc[i].idxmax(axis=1)
            similarity_matrix.loc[i][max_col] = -1
            if max_col != i:
                tmp[1].append(max_col)
                j += 1
        k_nearest.append(tmp)
    return k_nearest

client = MongoClient('localhost', 27017)
db = client.test
doc_col = db.doc
recommend_col = db.recommend

dt_matrix = get_dt_matrix(doc_col.find(), 20)
k_matrix = get_k_matrix(dt_matrix, 5)
for k in k_matrix:
    recommend_list = []
    for i in k[1]:
        doc = doc_col.find_one({'title': i})
        recommend_list.append({'title': i, 'url': doc['_id']})
    recommend_col.save({'_id': k[0], 'recommend': recommend_list})
