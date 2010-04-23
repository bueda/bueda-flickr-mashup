from django.test.client import Client
from nose.tools import assert_equal

def test_html_demo_prompt():
    c = Client()
    response = c.get('/flickr/')
    assert response

def test_html_demo_result():
    c = Client()
    response = c.get('/flickr/?username=aayushkumar')
    assert response

def test_json_missing_username():
    c = Client()
    response = c.get('/flickr/', HTTP_ACCEPT="application/json")
    assert response
    assert_equal(response['Content-Type'], 'application/json')
    assert_equal(response.status_code, 400)

def test_json_result():
    c = Client()
    response = c.get('/flickr/?username=aayushkumar', HTTP_ACCEPT="application/json")
    assert response
    assert_equal(response['Content-Type'], 'application/json')
