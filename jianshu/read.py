import os
import jieba
from pymongo import MongoClient

from jianshu.doc import Doc

sum_n = 0
postings_lists = {}
client = MongoClient('localhost', 27017)
db = client.test
doc_col = db.doc
config_col = db.doc_config
relation_col = db.relation
files = doc_col.find()
files_count = files.count()
for file in files:
    n = 0
    word_dict = {}
    _id = file['_id']
    title = file['title']
    content = file['content']
    time = file['time']
    word_list = jieba.lcut_for_search(title + '。' + content)
    for word in word_list:
        n += 1
        if word in word_dict:
            word_dict[word] += 1
        else:
            word_dict[word] = 1
    sum_n += n
    for key, value in word_dict.items():
        d = Doc(title, time, value, n, _id)
        if key in postings_lists:
            postings_lists[key][0] += 1
            postings_lists[key][1].append(d)
        else:
            postings_lists[key] = [1, [d]]
avg_n = sum_n / files_count
config_col.insert({'_id': 1, 'N': files_count, 'avg_n': avg_n})

for key, value in postings_lists.items():
    doc_list = '\n'.join(map(str, value[1]))
    relation_col.insert({'key': key, 'number': value[0], 'doc_list': doc_list})
