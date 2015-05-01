# Create your views here.
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
import json
from graph.graph import Graph
from graph.rules import *
import codecs
import os.path
import base64


class IndexView(TemplateView):
    template_name = 'index.html'

graph = Graph()
filename = os.path.realpath('data/processed-data.csv')
graph.load(filename)


def search_resource(query, index):
    query = query.lower()
    triples = graph.triples(None, None, None)
    result = set()
    for t in triples:
        if query in t[index].lower():
            result.add(t[index])
    return list(result)


@csrf_exempt
def infer_types(request):
    if request.method == "POST":
        graph.apply_inference(TypeRule())

        return HttpResponse(
            json.dumps({"state": "success"}),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"state": "failed"}),
            content_type="application/json"
        )


@csrf_exempt
def infer_parents(request):
    if request.method == "POST":
        graph.apply_inference(ParentSpeciesRule())

        return HttpResponse(
            json.dumps({"state": "success"}),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"state": "failed"}),
            content_type="application/json"
        )


@csrf_exempt
def suggest_subject(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')

        return HttpResponse(
            json.dumps({"query": query, "suggestions": search_resource(query, 0)}),
            content_type="application/json"
        )


@csrf_exempt
def suggest_predicate(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')

        return HttpResponse(
            json.dumps({"query": query, "suggestions": search_resource(query, 1)}),
            content_type="application/json"
        )


@csrf_exempt
def suggest_object(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')

        return HttpResponse(
            json.dumps({"query": query, "suggestions": search_resource(query, 2)}),
            content_type="application/json"
        )


@csrf_exempt
def search(request):
    if request.method == "POST":
        reader = codecs.getreader("utf-8")
        data = json.load(reader(request))

        print(data)

        # obtain resulting triples
        results = graph.triples(data['subject'], data['predicate'], data['object'])

        # create graph from results as the file 'graph.png'
        graph.create_graph(results)

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

