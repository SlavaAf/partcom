#coding: utf-8
from django.shortcuts import render, redirect
from catalog.forms import SearchPartForm
from catalog.models import *
from django.views.generic import ListView, DetailView


class PartsView(ListView):
    model = Part

    def get_queryset(self):
        shop = self.request.user.profile.shop.get()
        return shop.parts.all()


class PartDetailView(DetailView):
    model = Part
    template_name = 'accounts/parts_detail.html'

    def get_queryset(self):
        shop = self.request.user.profile.shop.get()
        return shop.parts.all()


def search_by_article(request):

    form = SearchPartForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        part = Part.objects.filter(article__contains=form.cleaned_data.get("article").strip())
        object_list = PartsInShop.objects.filter(part=part)
        return render(request, 'catalog/search_result.html', {'object_list': object_list})
    else:
        return render(request, 'catalog/search_result.html')


def part_detail(request, slug):
    part_del_end = 0
    if request.method == 'POST':
        obj = request.POST.get('PK')
        object_list = PartsInShop.objects.get(pk=obj)
        order_list = object_list.shop.profile.shop.first().pd_dis.all()
        part_del_fail = order_list.filter(state_in_part='pd_fail').count()
        for order in order_list:
            if order.part_del.state == 'ts_ended':
                part_del_end += 1
        stat_list = {'part_del_end': part_del_end, 'part_del_fail': part_del_fail}
        return render(request, 'catalog/part_detail.html', dict(object_list=object_list, stat_list=stat_list))
    else:
        return redirect('/catalog/')


def part_list_view(request):
    object_list = PartsInShop.objects.all()
    return render(request, 'catalog/catalog.html', {'object_list': object_list})