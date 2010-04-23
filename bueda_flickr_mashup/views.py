from django.views.generic.simple import direct_to_template
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest

import flickrapi
import flickrapi.shorturl
import simplejson
import bueda
import logging
 
def demo(request):
    flickr_conn = flickrapi.FlickrAPI(settings.FLICKR_API_KEY,
        settings.FLICKR_API_SECRET)       

    username = request.GET.get('username', '')
    if username:
        response = flickr_conn.people_findByUsername(
                username=request.GET.get('username', ''))
        user_id = response.find('user').attrib['id']

        response = flickr_conn.people_getPublicPhotos(user_id=user_id)
        public_photos = response.find('photos').findall('photo')[0:5]
        enriched_photos = []
        for photo in public_photos:
            photo_id = photo.attrib['id']
            short_url = "http://flic.kr/p/%s" % flickrapi.shorturl.encode(
                    photo_id)

            response = flickr_conn.tags_getListPhoto(photo_id=photo_id)
            xml_tags = response.find('photo').find('tags').findall('tag')
            tags = []
            for xml_tag in xml_tags:
                tags.append(xml_tag.attrib['raw'])
            enriched_tags = bueda.enrich(tags)

            img_url = "http://farm%s.static.flickr.com/%s/%s_%s_m.jpg" % (
                    photo.attrib['farm'],
                    photo.attrib['server'],
                    photo_id,
                    photo.attrib['secret'])

            output_tags = enriched_tags.canonical
            output_tags.extend(map(lambda c: c.name, enriched_tags.categories))
            for concept in enriched_tags.semantic:
                output_tags.extend(concept.types)
            output_tags = set(output_tags)

            enriched_photos.append(dict(img_url=img_url, page_url=short_url,
                    original_tags=tags,
                    tags=output_tags))

        if 'application/json' in request.META.get('HTTP_ACCEPT', ''):
            return HttpResponse(simplejson.dumps(enriched_photos),
                mimetype='application/json')
        else:
          return direct_to_template(request,
                'bueda_flickr_mashup/templates/bueda_flickr_mashup/demo.html',
                {'photos': enriched_photos})
    else:
      if 'application/json' in request.META.get('HTTP_ACCEPT', ''):
          return HttpResponseBadRequest(mimetype='application/json')
      else:
          return direct_to_template(request,
                'bueda_flickr_mashup/templates/bueda_flickr_mashup/demo.html')
