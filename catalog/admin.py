#coding: utf-8
from django.contrib import admin
from catalog.models import *

class PartAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("article",)}
    list_display = ('article', 'title')
    search_fields = ['article', 'title']


class PartInShopAdmin(admin.ModelAdmin):
    raw_id_fields = ['part', 'shop']
    list_display = ('part', 'shop', 'price', 'count')

admin.site.register(Part, PartAdmin)
admin.site.register(PartsInShop, PartInShopAdmin)