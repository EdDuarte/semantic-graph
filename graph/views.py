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

@csrf_exempt
def suggestSubject(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')

        return HttpResponse(
            json.dumps({"query": query, "suggestions": ["a", "b", "c"]}),
            content_type="application/json"
        )

def suggestObject(request):
    return ""

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
        # image = Image.open(graph_file_name)

        # serialize image to HTTP response
        # buffer = io.BytesIO()
        # image.save(buffer, format="PNG")
        return HttpResponse(
            base64.encodestring(open(graph_file_name,"rb").read())
        )

        # post = Post.objects.get(pk=int(QueryDict(request.body).get('postpk')))
        #
        # post.delete()

        # response_data = {}
        # response_data['msg'] = 'Post was deleted.'
        #
        # return HttpResponse(
        #     json.dumps(response_data),
        #     content_type="application/json"
        # )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )