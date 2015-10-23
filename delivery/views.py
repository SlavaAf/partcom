#coding: utf-8
from importlib import import_module
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
import json
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
import redis
from delivery.models import *
from catalog.models import *
from accounts.models import *
from django.views.generic import ListView, DetailView
from delivery.forms import *
from django import forms


def order_view(request):
    a = ''
    if request.method == 'POST':
        if 'ts_created' in request.POST:
            a = 'ts_created'
        if 'ts_accept' in request.POST:
            a = 'ts_accept'
        if 'ts_buy' in request.POST:
            a = 'ts_buy'
        if 'ts_ended' in request.POST:
            a = 'ts_ended'
        object_list = request.user.profile.dd_client.filter(state=a)
        return render(request, 'accounts/delivery.html', {'object_list': object_list})
    else:
        object_list = request.user.profile.dd_client.all()
        return render(request, 'accounts/delivery.html', {'object_list': object_list})


class OrderDetail(DetailView):
    model = Delivery
    template_name = 'accounts/order_detail.html'

    def get_queryset(self):
        return self.model.objects.all()


def ajax_add_to_cart(request):
    if request.is_ajax():
        pk = int(request.GET.get('cart_part_id', None))
        obj = PartsInShop.objects.get(pk=pk)
        if not 'cart' in request.session:
            request.session['cart'] = {}
        if obj.count >= 1:
            if request.user.is_authenticated() and (obj.shop in request.user.profile.shop.all()):
                return HttpResponse(json.dumps({'error_code': 0, 'code_add': 2}), content_type='application/json')
            else:
                if str(obj.id) in request.session['cart']:
                    if obj.count > request.session['cart'][str(obj.id)]['count']:
                        request.session['cart'][str(obj.id)]['count'] += 1
                        request.session['cart'][str(obj.id)]['price'] = request.session['cart'][str(obj.id)]['count'] * int(obj.price)
                        request.session.save()
                        # PartsInShop.objects.filter(pk=pk).update(count=(obj.count-1))
                    else:
                        return HttpResponse(json.dumps({'error_code': 0, 'code_add': 3}), content_type='application/json')
                else:
                    request.session['cart'][str(obj.id)] = {'title': obj.part.title, 'count': 1, 'article': obj.part.article, 'cost': str(obj.price), 'id': obj.id}
                    request.session['cart'][str(obj.id)]['price'] = request.session['cart'][str(obj.id)]['count'] * int(obj.price)
                    request.session.save()
                    # PartsInShop.objects.filter(pk=pk).update(count=(obj.count-1))
                return HttpResponse(json.dumps({'error_code': 0, 'code_add': 0, 'part_count': obj.count}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'error_code': 0, 'code_add': 1}), content_type='application/json')
    else:
        return redirect(reverse_lazy('account_index'))


def show_cart(request):
    amount = 0
    if not 'cart' in request.session:
        request.session['cart'] = {}
        request.session.save()
    object_list = request.session['cart'].values()
    for object in object_list:
        amount += int(object.get('price'))
    return render(request, 'accounts/user_cart.html', {'object_list': object_list, 'amount_list': amount})


def ajax_delete_to_cart(request):
    if request.is_ajax():
        pk = str(request.GET.get('cart_part_id', None))
        if pk in request.session['cart']:
            # count = request.session['cart'][pk]['count']
            # obj_count = PartsInShop.objects.get(pk=pk).count
            # PartsInShop.objects.filter(pk=pk).update(count=(obj_count+count))
            del request.session['cart'][pk]
            request.session.save()
            if request.session['cart'].__len__() == 0:
                code_a = 1
            else:
                code_a = 0
            return HttpResponse(json.dumps({'error_code': 0, 'code_del': code_a}), content_type='application/json')
    else:
        return redirect(reverse_lazy('ajax_delete_to_cart'))


def ajax_plus_to_cart(request):
    if request.is_ajax():
        pk = request.GET.get('cart_part_id', None)
        amount = 0
        if pk in request.session['cart']:
            if PartsInShop.objects.get(pk=int(pk)).count > request.session['cart'][pk]['count']:
                request.session['cart'][pk]['count'] += 1
                count = request.session['cart'][pk]['count']
                # obj_count = PartsInShop.objects.get(pk=pk).count
                # PartsInShop.objects.filter(pk=pk).update(count=(obj_count-1))
                price = int(PartsInShop.objects.get(pk=int(pk)).price) * count
                request.session['cart'][pk]['price'] = price
                object_list = request.session['cart'].values()
                for object in object_list:
                    amount += int(object.get('price'))
                request.session.save()
                return HttpResponse(json.dumps({'error_code': 0, 'part_count': count, 'part_price': price,
                                        'amount_price': amount, 'code_plus': 1}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({'error_code': 0, 'code_plus': 0}), content_type='application/json')
    else:
        return redirect(reverse_lazy('ajax_plus_to_cart'))


def ajax_minus_to_cart(request):
    if request.is_ajax():
        amount = 0
        pk = request.GET.get('cart_part_id', None)
        if pk in request.session['cart']:
            if request.session['cart'][pk]['count'] > 1:
                request.session['cart'][pk]['count'] -= 1
                count = request.session['cart'][pk]['count']
                # obj_count = PartsInShop.objects.get(pk=pk).count
                # PartsInShop.objects.filter(pk=pk).update(count=(obj_count+1))
                price = int(PartsInShop.objects.get(pk=int(pk)).price) * count
                request.session['cart'][pk]['price'] = price
                object_list = request.session['cart'].values()
                for object in object_list:
                    amount += int(object.get('price'))
                request.session.save()
                return HttpResponse(json.dumps({'error_code': 0, 'part_count': count, 'part_price': price,
                                        'amount_price': amount, 'code_min': 0}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({'error_code': 0, 'code_min': 1}), content_type='application/json')
    else:
        return redirect(reverse_lazy('ajax_minus_to_cart'))


def checkout_cart(request):
    c = 0
    shippingform = ShippingForm(request.POST or None, prefix='ShippingForm')
    paymentform = PaymentForm(request.POST or None, prefix='PaymentForm')
    addresshipform = AddressForm(request.POST or None, prefix='AddresShipForm')
    object_list = request.user.profile.addresses.all()
    if request.method == 'POST' and (shippingform.is_valid() and paymentform.is_valid()):
        ship = request.POST.get('ShippingForm-shipping')
        pay = request.POST.get('PaymentForm-payment')
        item_list = request.session['cart'].values()
        for item in item_list:
            c += int(item.get('price'))
        if ship == 'td_courier':
            if 'checkout_btn_new' in request.POST:
                if addresshipform.is_valid():
                    a = addresshipform.save()
                    a.profiles.add(request.user.profile)
                    a.save()
                    o = Delivery.objects.create(client_del=request.user.profile, amount=c, state='ts_created', payment=pay, shipping=ship, address_id=a.pk)
                else:
                    messages.error(request, 'Вы ввели неправильно данные при создании адреса!')
                    return render(request, 'accounts/checkout_cart.html', dict(ShippingForm=shippingform, PaymentForm=paymentform,
                                                                   AddresShipForm=addresshipform, object_list=object_list))
            else:
                for item in request.user.profile.addresses.all():
                    if 'checkout_btn_'+str(item.pk) in request.POST:
                        o = Delivery.objects.create(client_del=request.user.profile, amount=c, state='ts_created',
                                                    payment=pay, shipping=ship, address_id=item.pk)
        else:
            o = Delivery.objects.create(client_del=request.user.profile, amount=c, state='ts_created', payment=pay, shipping=ship)
        for item in item_list:
            o.ps_del.create(quantity=item.get('count'), part_in_shop_id=item.get('id')).del_in_shop.add(PartsInShop.objects.filter(pk=item.get('id')).get().shop)
            o.save()
            PartsInShop.objects.filter(pk=item.get('id')).update(count=(PartsInShop.objects.get(pk=item.get('id')).count - item.get('count')))
        del request.session['cart']
        messages.success(request, 'Вы успешно создали заказ!')
        return redirect('/account/')
    else:
        return render(request, 'accounts/checkout_cart.html', dict(ShippingForm=shippingform, PaymentForm=paymentform, AddresShipForm=addresshipform, object_list=object_list))


def ajax_badge_cart(request):
    if request.is_ajax():
        badge_cart = ''
        if 'cart' in request.session:
            if request.session['cart']:
                badge_cart = request.session['cart'].__len__()
        else:
            request.session['cart'] = {}

        # Unread messages control
        try:
            chats = request.user.profile.chats.all()
        except AttributeError:
            chats = []
        r = redis.Redis('localhost')
        unread_chats = []
        chat_count = 0
        for chat in chats:
            messages_list = []
            unread_chat = {'chat_pk': chat.pk, 'count': 0}
            channel = 'channel_' + str(chat.pk)
            messages = r.lrange(channel, 0, r.llen(channel))
            for message in messages:
                messages_list.append(eval(message))
            for list_item in messages_list:
                if not request.user.profile.pk in list_item['read']:
                    unread_chat['count'] += 1
            unread_chats.append(unread_chat)
        for item in unread_chats:
            if item['count'] != 0:
                chat_count += 1
        return HttpResponse(json.dumps({'error_code': 0, 'badge_cart': badge_cart, 'chat_count': chat_count, 'unread_chats': unread_chats}), content_type='application/json')
    else:
        return redirect(reverse_lazy('ajax_badge_cart'))


def ajax_validation_cart(request):
    if request.is_ajax():
        part_list = []
        cost_list = []
        count_list = {}
        price_list = {}
        amount = 0
        otvet = 0
        item_list = request.session['cart'].values()
        st = request.GET.get('stat', None)
        pk = request.GET.get('pk', None)
        if st == 'fail':
            for item in item_list:
                count = PartsInShop.objects.get(id=item.get('id')).count
                price = PartsInShop.objects.get(id=item.get('id')).price
                if item.get('count') > count:
                    part_list.append(item.get('id'))
                    count_list[item.get('id')] = count
                if item.get('cost') != str(price):
                    cost_list.append(item.get('id'))
                    price_list[item.get('id')] = str(price)
            if (part_list and cost_list)or(part_list or cost_list):
                return HttpResponse(json.dumps({'error_code': 0,
                                            'part_list': part_list, 'count': count_list,
                                            'cost_list': cost_list, 'price': price_list}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({'error_code': 0, 'code_a': 1}), content_type='application/json')
        if st == 'ok':
            cost = PartsInShop.objects.get(id=pk).price
            request.session['cart'][pk]['cost'] = str(cost)
            count = request.session['cart'][pk]['count']
            price = int(PartsInShop.objects.get(pk=int(pk)).price) * count
            request.session['cart'][pk]['price'] = price
            for item in item_list:
                amount += int(item.get('price'))
            request.session.save()
            return HttpResponse(json.dumps({'error_code': 0, 'cost': str(cost), 'part_price': str(price), 'amount_price': str(amount)}), content_type='application/json')
    else:
        # return redirect(reverse_lazy('account_index'))
        return HttpResponse(json.dumps({'error_code': 1}), content_type='application/json')
