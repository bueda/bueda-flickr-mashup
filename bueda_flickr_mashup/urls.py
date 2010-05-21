from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url('^$','django.views.generic.simple.direct_to_template',{'template':'bueda_flickr_mashup/templates/bueda_flickr_mashup/demo.html'},name='demo'),
    url('^run','views.demo',name='run'),
)
