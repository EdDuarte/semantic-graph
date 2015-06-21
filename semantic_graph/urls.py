__author__ = 'Ed Duarte'
__email__ = "edmiguelduarte@gmail.com"
__copyright__ = "Copyright 2015, Ed Duarte"
__credits__ = ["Ed Duarte"]

__license__ = "Apache License 2.0"
__version__ = "2.0.0"
__maintainer__ = "Ed Duarte"
__status__ = "Prototype"

from django.conf.urls import patterns, url
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

from graph.views import *



# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = patterns('',
                       url(r'^$',
                           TemplateView.as_view(template_name="index.html")),
                       url(r'^index.html',
                           TemplateView.as_view(template_name="index.html")),
                       url(r'^suggest_subject/$', suggest_subject),
                       url(r'^suggest_predicate/$', suggest_predicate),
                       url(r'^suggest_object/$', suggest_object),
                       url(r'^search/$', search),
                       url(r'^infer_types/$', infer_types),
                       url(r'^infer_parents/$', infer_parents),
                       url(r'^upload/$', upload),
                       url(r'^export/$', export),
                       url(r'^add/$', add),
                       url(r'^remove/$', remove),
                       url(r'^is_ready/$', is_ready)
                       )
