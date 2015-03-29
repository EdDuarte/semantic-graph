from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader
from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = 'index.html'