__author__ = 'Ed Duarte'
__email__ = "edmiguelduarte@gmail.com"
__copyright__ = "Copyright 2015, Ed Duarte"
__credits__ = ["Ed Duarte"]

__license__ = "Apache License 2.0"
__version__ = "2.0.0"
__maintainer__ = "Ed Duarte"
__status__ = "Prototype"

import json
import codecs
import os
import base64

from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.core.servers.basehttp import FileWrapper

from graph.graph import Graph
from graph.rules import *


class IndexView(TemplateView):
    template_name = 'index.html'


graph = Graph()

def search_resource(query, index):
    query = query.lower()
    triples = graph.triples(None, None, None)
    results = []
    for t in triples:
        if query in t[index].lower():
            results.append(t[index])
    results = unique(results)
    if len(results) is not 0:
        results = sorted(results)
    return results


def search_predicates(query):
    query = query.lower()
    results = []
    for p in graph.predicates():
        if query in p.lower():
            results.append(p)
    results = unique(results)
    if len(results) is not 0:
        results = sorted(results)
    return results


def unique(iterable):
    seen = set()
    return [seen.add(x) or x for x in iterable if x not in seen]


@csrf_exempt
def suggest_subject(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')

        return HttpResponse(
            json.dumps(
                {"query": query, "suggestions": search_resource(query, 0)}),
            content_type="application/json"
        )


@csrf_exempt
def suggest_predicate(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')

        return HttpResponse(
            json.dumps(
                {"query": query, "suggestions": search_predicates(query)}),
            content_type="application/json"
        )


@csrf_exempt
def suggest_object(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')

        return HttpResponse(
            json.dumps(
                {"query": query, "suggestions": search_resource(query, 2)}),
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
            sub = d['subject']
            pre = d['predicate']
            obj = d['object']
            r = graph.triples(sub, pre, obj)
            l.append(r)

        # flatten results
        l = [item for sublist in l for item in sublist]

        if len(l) == 0:
            return HttpResponse()

        # create graph from results as the file 'graph.png'
        graph.draw_graph(l)

        # open the image created above
        graph_file_name = os.path.realpath('graph.png')

        # serialize image to Base64
        return HttpResponse(
            base64.encodestring(open(graph_file_name, "rb").read())
        )

@csrf_exempt
def suggest_entity(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')
        query = query.lower()
        triples = graph.triples(None, None, None)
        results = []
        for t in triples:
            if query in t[0].lower():
                results.append(t[0])

            if query in t[2].lower():
                results.append(t[2])
        results = unique(results)
        if len(results) is not 0:
            results = sorted(results)

        return HttpResponse(
            json.dumps(
                {"query": query, "suggestions": results}),
            content_type="application/json"
        )

@csrf_exempt
def search_entity(request):
    if request.method == "POST":
        reader = codecs.getreader("utf-8")
        data = json.load(reader(request))
        entity = data['entity']
        if entity is None or entity.strip().isspace():
            return HttpResponse("")

        (subject_data, object_data) = graph.browse(entity)

        # serialize strings
        return HttpResponse(json.dumps({
            "subjectResults": subject_data,
            "objectResults": object_data
        }))


@csrf_exempt
def infer_types(request):
    if request.method == "GET":
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
    if request.method == "GET":
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
def upload(request):
    if request.method == "POST":
        reader = codecs.getreader("utf-8")
        data = json.load(reader(request))

        try:
            # get request base64 file
            file_content = base64.decodestring(bytes(data['base'], "utf-8"))
            file_format = data['format']

            # # save binary bytes into a local file
            # f = open("upload-input", "w")
            # f.write(file_content.decode("utf-8"))
            # f.close()
            #
            # # send local file path to graph according to format
            # file_name = os.path.realpath('upload-input')
            graph.load(file_content, file_format)

            # output success state
            return HttpResponse(
                json.dumps({"state": "success"}),
                content_type="application/json"
            )

        except Exception as e:
            return HttpResponse(
                json.dumps({"state": "failed", "message": str(e)}),
                content_type="application/json"
            )
    else:
        return HttpResponse(
            json.dumps({"state": "failed", "message": "Request was not POST!"}),
            content_type="application/json"
        )


@csrf_exempt
def export(request):
    if request.method == "POST":
        reader = codecs.getreader("utf-8")
        data = json.load(reader(request))

        # get request file format
        file_format = data['format']

        # save graph into a local file
        file_name = os.path.realpath("export-output")
        graph.save(file_name, file_format)

        ext = file_format
        if file_format == "nt":
            ct = "text/nt"
        elif file_format == "n3":
            ct = "text/n3"
        elif file_format == "pretty-xml":
            ct = "application/rdf+xml"
            ext = "rdf"
        # elif file_format == "sqlite3":
        #     ct = "file/sqlite3"
        else:
            ct = "text/plain"

        # serve local file to client
        # if file_format == "sqlite3":
        #     file = File(open(file_name, "rb"))
        #     response = HttpResponse(file, content_type='application/x-sqlite3')
        #     response['Content-Length'] = file.size
        # else:
        wrapper = FileWrapper(open(file_name, "rb"))
        response = HttpResponse(wrapper, content_type=ct)
        response['Content-Length'] = os.path.getsize(file_name)
        response['Content-Disposition'] = 'attachment; filename=export.' + ext
        return response


@csrf_exempt
def add(request):
    if request.method == "POST":
        reader = codecs.getreader("utf-8")
        data = json.load(reader(request))

        sub = data['subject']
        pre = data['predicate']
        obj = data['object']

        try:
            graph.add(sub, pre, obj)
        except Exception as e:
            return HttpResponse(
                json.dumps({"state": "failed", "message": str(e)}),
                content_type="application/json"
            )

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
def remove(request):
    if request.method == "POST":
        reader = codecs.getreader("utf-8")
        data = json.load(reader(request))

        sub = data['subject']
        pre = data['predicate']
        obj = data['object']

        try:
            graph.remove(sub, pre, obj)
        except Exception as e:
            return HttpResponse(
                json.dumps({"state": "failed", "message": str(e)}),
                content_type="application/json"
            )

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
def is_ready(request):
    if request.method == "GET":

        return HttpResponse(
            json.dumps({"state": "success", "result": graph.has_triples()}),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"state": "failed", "result": False}),
            content_type="application/json"
        )

