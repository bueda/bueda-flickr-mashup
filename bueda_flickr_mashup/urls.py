from django.conf.urls.defaults import *

urlpatterns = patterns('flickr.views',
    url(r'^$', 'demo', name='demo'),
)
