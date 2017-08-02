from django.shortcuts import render

from jianshu import recommend
from . import bm
from jianshu.entity.doc import Doc
from pymongo import MongoClient


# Create your views here.


def say_hello(request):
    return render(request, 'index.html', {'content': 'HelloWorld!'})


def search(request):
    return render(request, 'search.html', {'show': True})


def search_keyword(request):
    client = MongoClient('localhost', 27017)
    db = client.test
    doc_col = db.doc
    recommend_col = db.recommend
    result = {}
    keyword = request.POST['key_word']
    result['key'] = keyword
    scores = bm.bm25(keyword)
    docs = []
    if len(scores) == 0:
        result['show'] = False
    else:
        for item in scores:
            d = doc_col.find_one({'title': item[0]})
            r = recommend_col.find_one({'_id': item[0]})
            doc = Doc(item[0], item[1], d['time'], d['_id'], d['snippet'], r['recommend'])
            docs.append(doc)
            result['docs'] = docs
            result['show'] = True
    return render(request, 'search.html', result)
