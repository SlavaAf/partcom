#coding: utf-8
from django.contrib import admin
from delivery.models import *
from accounts.models import *
from catalog.models import *


class DeliveryInline(admin.TabularInline):
    raw_id_fields = ['part_in_shop', 'part_del', 'del_in_shop', ]
    model = PartInDelivery
    extra = 1


class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('client_del', 'shipping', 'payment', 'state', 'amount', 'address')
    raw_id_fields = ['client_del', 'parts_in_del', ]
    search_fields = ['client_del', ]
    inlines = (DeliveryInline,)


class PartInDeliveryAdmin(admin.ModelAdmin):
    list_display = ('quantity', )
    raw_id_fields = ['part_in_shop', 'del_in_shop']


admin.site.register(Delivery, DeliveryAdmin)
admin.site.register(PartInDelivery, PartInDeliveryAdmin)