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
is_graph_ready = False


def search_resource(query, index):
    query = query.lower()
    triples = graph.triples(None, None, None)
    results = []
    for t in triples:
        if query in t[index].lower():
            results.append(t[index])
    return unique(results)


def unique(iterable):
    seen = set()
    return [seen.add(x) or x for x in iterable if x not in seen]


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

        # obtain resulting triples
        l = []
        for d in data:
            r = graph.triples(d['subject'], d['predicate'], d['object'])
            l.append(r)

        # flatten results
        l = [item for sublist in l for item in sublist]

        # create graph from results as the file 'graph.png'
        graph.create_graph(l)

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


@csrf_exempt
def upload(request):
    global is_graph_ready
    if request.method == "POST":
        reader = codecs.getreader("utf-8")
        data = json.load(reader(request))

        try:
            # get request base64 file
            file_bytes = base64.decodestring(bytes(data['base'], "utf-8"))
            format = data['format']

            # save binary bytes into a local file
            f = open("upload-input", "w")
            f.write(file_bytes.decode("utf-8"))
            f.close()

            # send local file path to graph according to format
            filename = os.path.realpath('upload-input')
            graph.load(filename)
            is_graph_ready = True

        except Exception as e:
            return HttpResponse(
                json.dumps({"state": "failed", "message": str(e)}),
                content_type="application/json"
            )

        # serialize image to Base64
        return HttpResponse(
            json.dumps({"state": "success"}),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"state": "failed", "message": "Request was not POST!"}),
            content_type="application/json"
        )


@csrf_exempt
def is_ready(request):
    if request.method == "GET":
        return HttpResponse(
            json.dumps({"state": "success", "result": is_graph_ready}),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"state": "failed", "result": False}),
            content_type="application/json"
        )

