#coding: utf-8
import time
import json
import urllib2
from datetime import datetime
from django import forms
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse
from django.template.context import RequestContext
from django_sse.redisqueue import send_event, RedisQueueView
import redis
from catalog.models import *
from delivery.models import *
from partcom.backends import Backend
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.views.generic import RedirectView, ListView, DetailView
from accounts.forms import *
import string, random
from accounts.models import UserProfile, Client, Chat, Shop, Post
from django.forms.util import ErrorList
from pytils.translit import slugify
from django.contrib import messages


def generate_user_password(n):
    length = n
    chars = string.ascii_lowercase + string.digits
    code = ''.join(random.choice(chars) for i in range(length))
    return code


def authentication(request):
    form = AuthSendSmsForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        try:
            user = UserProfile.objects.get(phone=form.cleaned_data['phone'])
            user.sms_code = random.randint(100000, 999999)
            user.save()
            urllib2.urlopen('http://smsc.ru/sys/send.php?login=Jango.kz&psw=AcEMXtLGz042Fc1ZJUSl&phones=+' + user.phone + '&mes=Access code: ' + str(user.sms_code))
            return redirect('/account/login/?phone='+user.phone)
        except UserProfile.DoesNotExist:
            return redirect('/account/registration/?phone='+form.cleaned_data['phone'])
    else:
        return render(request, 'accounts/authentication.html', {'form': form})


def registration(request):
    form = AuthRegistrationForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user_id = User.objects.all().aggregate(Max('id'))['id__max'] + 1
        username = 'User' + str(user_id)
        try:
            user = User.objects.create_user(username=username,
                                            password=generate_user_password(16),
                                            email=form.cleaned_data['email'],
                                            first_name=form.cleaned_data['first_name'],
                                            last_name=form.cleaned_data['last_name'])
        except IntegrityError:
            user_id = User.objects.all().aggregate(Max('id'))['id__max'] + 1
            username = 'User' + str(user_id)
            user = User.objects.create_user(username=username,
                                            password=generate_user_password(16),
                                            email=form.cleaned_data['email'],
                                            first_name=form.cleaned_data['first_name'],
                                            last_name=form.cleaned_data['last_name'])
        user_profile = UserProfile.objects.create(user=user, phone=request.GET.get('phone'), sms_code=random.randint(100000, 999999), account_type=form.cleaned_data['account_type'])
        urllib2.urlopen('http://smsc.ru/sys/send.php?login=Jango.kz&psw=AcEMXtLGz042Fc1ZJUSl&phones=+' + user_profile.phone + '&mes=Access code: ' + str(user_profile.sms_code))
        Client.objects.create(profile=user_profile)
        return redirect('/account/login/?phone='+user_profile.phone)
    else:
        return render(request, 'accounts/registration.html', {'form': form})


def user_login(request):
    form = AuthInputCodeForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        cart = {}
        user = UserProfile.objects.get(phone=request.GET.get('phone'))
        if form.cleaned_data['code'] == user.sms_code:
            auth_user = Backend().authenticate(phone=user.phone, sms_code=user.sms_code)
            if 'cart' in request.session:
                cart = request.session['cart']
            login(request, auth_user)
            if not 'cart' in request.session:
                request.session['cart'] = cart
                request.session.save()
            auth_user.profile.sms_code = '2517'
            auth_user.profile.save()
            return redirect('/account')
        else:
            errors = form._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.util.ErrorList())
            errors.append(u"Вы ввели неправильный код")
            return render(request, 'accounts/login.html', {'form': form})
    else:
        return render(request, 'accounts/login.html', {'form': form})


class LogOutView(RedirectView):
    permanent = False
    url = reverse_lazy('index')

    def get_redirect_url(self):
        logout(self.request)
        return self.url


class DialogsView(ListView):
    model = Chat

    def get_queryset(self):
        chats = self.request.user.profile.chats.all()
        return chats


def chat_control_view(request, u_pk):
    if request.user.profile.pk == int(u_pk):
        return redirect('/account/')
    ps = UserProfile.objects.filter(pk__in=[request.user.profile.pk, u_pk])
    chat = UserProfile.get_chats_with_user(ps[0], ps[1])
    if chat:
        return redirect('/account/chat/'+str(chat.pk))
    else:
        chat = Chat.objects.create()
        chat.users.add(ps[0].pk, ps[1].pk)
        return redirect('/account/chat/'+str(chat.pk))


def public_chat_view(request):
    public_chat = Chat.objects.get_or_create(pk=1)
    return redirect('/account/chat/'+str(public_chat[0].pk))


def search_user_view(request):
    users = {}
    if request.is_ajax() and 'user_search' in request.GET:
        q = request.GET.get('user_search', None)
        if q:
            for profile in UserProfile.objects.all():
                full_name = profile.get_fullname()
                if profile.pk not in users and q.lower() in full_name.lower() and users.__len__() <= 200 and profile != request.user.profile:
                    users[profile.pk] = {'full_name': full_name, 'pk': profile.pk}
        return HttpResponse(json.dumps({'error_code': 0, 'users': users}), content_type='application/json')
    return render(request, 'index.html')


def chat_add_user_view(request, pk, u_pk):
    chat = Chat.objects.get(pk=pk)
    try:
        chat.users.add(u_pk)
    except IntegrityError:
        pass
    return redirect('/account/chat/'+str(chat.pk))


def set_chat_title_view(request, pk):
    chat = Chat.objects.get(pk=pk)
    chat.title = request.GET.get("data")
    chat.save()
    return redirect('/account/chat/'+str(chat.pk))


def chat_view(request, pk):
    chat = Chat.objects.get(pk=pk)
    if request.user.profile in chat.users.all() or pk == '1':
        error_code = 0
        error_text = ''
        channel = 'channel_' + str(pk)
        SSE.redis_channel = channel
        if request.is_ajax() and request.method == 'GET' and request.GET.get("text").strip() != '':
                data = {
                    'u_pk': int(request.user.profile.pk),
                    'time': time.strftime("%H:%M:%S", time.localtime()),
                    'user': request.user.profile.get_fullname(),
                    'text': request.GET.get("text"),
                    'read': [int(request.user.profile.pk), ]
                }
                send_event("send_message", json.dumps(data), channel=SSE.redis_channel)
                r = redis.Redis('127.0.0.1')
                r.rpush(SSE.redis_channel, data)
                return HttpResponse(json.dumps({'error_code': error_code, 'error_text': error_text}), content_type="application/json")
        return render(request, 'accounts/chat.html', {'channel': channel, 'pk': pk, 'chat': chat})
    else:
        return redirect('/account/')


def get_messages(request, pk):
    error_code = 0
    error_text = ''
    channel = 'channel_' + str(pk)
    SSE.redis_channel = channel
    if request.is_ajax():
        r = redis.Redis('127.0.0.1')
        messages_list = []
        count = 0
        messages = r.lrange(SSE.redis_channel, 0, r.llen(SSE.redis_channel))
        for message in messages:
            messages_list.append(json.loads(message.replace('\'', '\"').replace('u"', '"')))
        for obj in messages_list:
            if not int(request.user.profile.pk) in obj['read']:
                i = messages_list.index(obj)
                obj['read'].append(int(request.user.profile.pk))
                r.lset(SSE.redis_channel, i, obj)
                count += 1
        if messages_list.__len__() > 20:
            if count == 0:
                messages_list = messages_list[-20:]
            else:
                messages_list = messages_list[-count-5:]
        return HttpResponse(json.dumps({'error_code': error_code, 'error_text': error_text, 'messages': messages_list}), content_type="application/json")
    return render(request, 'accounts/chat.html')


class SSE(RedisQueueView):
    def get_redis_channel(self):
        return self.kwargs['channel'] or self.redis_channel


class PostsListView(ListView):
    model = Post

    def get_queryset(self):
        object_list = self.model.objects.filter(is_public=True).order_by('-ts_created')
        return object_list


def post_list_view(request, u_pk):
    author = UserProfile.objects.get(pk=u_pk)
    if author.user == request.user:
        posts = Post.objects.filter(author=author).order_by('-ts_created')
    else:
        posts = Post.objects.filter(author=author, is_public=True).order_by('-ts_created')
    return render_to_response('accounts/post_list.html', {'object_list': posts, 'author': author}, context_instance=RequestContext(request))


def post_detail_view(request, u_pk, slug):
    post = Post.objects.get(slug=slug)

    if 'comment_text' in request.GET:
        if request.GET.get('comment_text').strip() != '':
            comment = PostComment.objects.create(post=post, user=request.user.profile, text=request.GET.get('comment_text'))
            if request.GET.get('comment_pk'):
                try:
                    comment_answered = PostComment.objects.get(pk=request.GET.get('comment_pk'))
                except PostComment.DoesNotExist:
                    return redirect('/blogs/'+str(post.author.pk)+'/'+str(slug))
                comment.answer_to = comment_answered
                comment.save()
            return redirect('/blogs/'+str(post.author.pk)+'/'+str(slug))
        else:
            messages.error(request, 'Комментарий не может быть пустым!')
    return render(request, 'accounts/post_detail.html', {'post': post, 'comments': post.comments.filter(answer_to=None)})


def add_post_view(request, slug):
    if slug == '0':
        form = AddPostForm(request.POST or None)
    else:
        post = Post.objects.get(slug=slug)
        form = AddPostForm(request.POST or None, initial={'content': post.content, 'title': post.title})
        if request.user != post.author.user:
            return redirect('/account/')

    if request.method == 'POST' and form.is_valid():
        if slug == '0':
            post = Post.objects.create(author=request.user.profile)
        else:
            post = Post.objects.get(slug=slug)
        post.content = form.cleaned_data['content']
        post.title = form.cleaned_data['title']
        post.slug = slugify(str(post.pk)+' '+form.cleaned_data['title'])
        post.save()
        return redirect('/blogs/'+str(request.user.profile.pk)+'/'+str(post.slug))
    return render(request, 'accounts/new_post.html', {'form': form, 'slug': slug})


def post_event_view(request, pk, event):
    post = Post.objects.get(pk=pk)

    if request.user == post.author.user:
        if event == 'unpublished':
            post.is_public = False
            post.save()
            return redirect('/blogs/'+str(request.user.profile.pk)+'/'+str(post.slug))
        if event == 'public':
            post.is_public = True
            post.ts_public = datetime.now()
            post.save()
            return redirect('/blogs/'+str(request.user.profile.pk)+'/'+str(post.slug))
        if event == 'edit':
            return redirect('/account/blog_new/'+str(post.slug))
        if event == 'delete':
            post.delete()
            return redirect('/account/blog/'+str(request.user.profile.pk))
    return render(request, 'accounts/post_detail.html', {'post': post, 'comments': post.comments.filter(answer_to=None)})


def account_index(request):
    shop = request.user.profile.shop.all()
    part_del = 0
    part_del_end = 0
    part_del_fail = 0
    part_del_ship = 0
    delivery_list = request.user.profile.dd_client.all()
    accept = delivery_list.filter(state='ts_accept').count()
    created = delivery_list.filter(state='ts_created').count()
    vsg = delivery_list.count()
    buy = delivery_list.filter(state='ts_buy').count()
    ended = delivery_list.filter(state='ts_ended').count()
    if shop:
        part_del = request.user.profile.shop.first().pd_dis.count()
        order_list = request.user.profile.shop.first().pd_dis.all()
        part_del_fail = order_list.filter(state_in_part='pd_fail').count()
        part_del_ship = order_list.filter(state_in_part='pd_ship').count()
        for order in order_list:
            if order.part_del.state == 'ts_ended':
                part_del_end += 1
    status_list = {'accept': accept, 'created': created, 'vsg': vsg, 'buy': buy, 'ended': ended, 'part_del': part_del,
                   'part_del_end': part_del_end, 'part_del_fail': part_del_fail, 'part_del_ship': part_del_ship}
    return render(request, 'accounts/index.html', {'status_list': status_list})


def part_add(request):
    form = AddPartForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        if request.POST.get('type') == 'on':
            a = 1
        else:
            a = 0
        o = Part.objects.create(article=request.POST.get('article'), title=request.POST.get('title'), slug=request.POST.get('article'))
        o.ps_parts.create(count=request.POST.get('count'), price=request.POST.get('price'), type=a, shop=request.user.profile.shop.get())
        return redirect('/account/')
    return render(request, 'accounts/part_add.html')


def part_delivery(request):
    part_del_end = 0
    form = StatePartDelForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        if 'ok' in request.POST.keys():
            PartInDelivery.objects.filter(id=request.POST.get('ok')).update(state_in_part='pd_ship')
        elif 'fail' in request.POST.keys():
            PartInDelivery.objects.filter(id=request.POST.get('fail')).update(state_in_part='pd_fail')
        return redirect('/account/part_delivery/')
    else:
        order_list = request.user.profile.shop.first().pd_dis.all()
        for order in order_list:
            if order.part_del.state == 'ts_ended':
                part_del_end += 1
        return render(request, 'accounts/part_delivery.html', {'order_list': order_list, 'end_part': part_del_end})


def edit_data_view(request, data):
    if data == 'main':
        form_user = EditUserDataForm(request.POST or None, instance=request.user)
        if request.method == 'POST' and form_user.is_valid():
            form_user.save()
            messages.success(request, 'Ваши данные успешно сохранены!')
            return redirect('/account/edit_data/main')
        else:
            return render(request, 'accounts/edit_data.html', dict(form=form_user))
    if data == 'contact':
        return render(request, 'accounts/edit_data.html', dict(form='', addresses=request.user.profile.addresses.all()))
    if data == 'personal':
        form_shop = EditShopDataForm(request.POST or None, instance=request.user.profile.shop.get())

        if request.method == 'POST' and form_shop.is_valid():
            form_shop.save()
            messages.success(request, 'Название магазина успешно сохранено!')
            return redirect('/account/edit_data/personal')
        else:
            return render(request, 'accounts/edit_data.html', dict(form=form_shop))
    else:
        return redirect('/account/')


def edit_address_view(request, pk):
    try:
        address = Address.objects.get(pk=pk)
        form_addresses = EditAddressesDataForm(request.POST or None, instance=address)
    except Address.DoesNotExist:
        form_addresses = EditAddressesDataForm(request.POST or None)

    if request.method == 'POST' and form_addresses.is_valid():
        request.user.profile.addresses.add(form_addresses.save())
        messages.success(request, 'Адрес успешно сохранен!')
        return redirect('/account/edit_data/contact')
    else:
        return render(request, 'accounts/edit_data.html', dict(form=form_addresses))


def delete_address_view(request, pk):
    address = Address.objects.get(pk=pk)
    if address in request.user.profile.addresses.all():
        address.delete()
        messages.success(request, 'Адрес успешно удален!')
    return redirect('/account/edit_data/contact')


def index_view(request):
    object_list = Post.objects.filter(is_public=True).order_by('-ts_created')[:3]
    part_list = PartsInShop.objects.all().order_by('-is_processing')[:10]
    return render(request, 'index.html', dict(object_list=object_list, part_list=part_list))
# Create your views here.
