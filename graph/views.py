from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
import json
from graph.grafo import Grafo
import codecs
import os.path
from PIL import Image
import base64
import io

class IndexView(TemplateView):
    template_name = 'index.html'

grafo = Grafo()
filename = os.path.realpath('taxon.csv')
grafo.load(filename)

def search_subjects(query):
    query = query.lower()
    triples = grafo.triples(None, None, None)
    result = list()
    for t in triples:
        if t[0].lower().startswith(query):
            result.append(t[0])
    return result

def search_object(query):
    query = query.lower()
    triples = grafo.triples(None, None, None)
    result = list()
    for t in triples:
        if t[2].lower().startswith(query):
            result.append(t[2])
    return result

@csrf_exempt
def suggestSubject(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')

        return HttpResponse(
            json.dumps({"query": query, "suggestions": search_subjects(query)}),
            content_type="application/json"
        )

def suggestObject(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')

        return HttpResponse(
            json.dumps({"query": query, "suggestions": search_object(query)}),
            content_type="application/json"
        )

@csrf_exempt
def search(request):
    if request.method == "POST":
        reader = codecs.getreader("utf-8")
        data = json.load(reader(request))

        print(data)

        # obtain resulting triples
        results = grafo.triples(data['subject'], data['predicate'], data['object'])

        # create graph from results as the file 'graph.png'
        grafo.create_graph(results)

        # open the image created above
        graph_file_name = os.path.realpath('graph.png')

        # serialize image to Base64
        return HttpResponse(
            base64.encodestring(open(graph_file_name,"rb").read())
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )