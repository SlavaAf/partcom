#coding: utf-8
from django.conf.urls import patterns, url
from catalog.views import *

urlpatterns = patterns('',
    url(r'^search_part/$', search_by_article, name='search_by_article'),
    url(r'^(?P<slug>[-_\w]+)/$', part_detail, name='catalog_part_detail'),
    url(r'^$', part_list_view, name='catalog_part')
)
