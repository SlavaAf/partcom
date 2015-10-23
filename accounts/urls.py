#coding: utf-8
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from accounts.views import *
from catalog.views import *
from delivery.views import *


urlpatterns = patterns('',
    url(r'^$', login_required(account_index), name='account_index'),
    url(r'^parts/$', login_required(PartsView.as_view(template_name='accounts/parts.html')), name='account_parts'),
    url(r'^auth/$', authentication, name='account_auth'),
    url(r'^login/$', user_login, name='account_login'),
    url(r'^parts/(?P<slug>[-_\w]+)/$', login_required(PartDetailView.as_view()), name='account_partsdetail'),
    url(r'^order/$', login_required(order_view), name='account_delivery'),
    url(r'^order/detail_order/(?P<pk>[-_\w]+)/$', login_required(OrderDetail.as_view()), name='account_order_detail'),
    url(r'^logout/$', LogOutView.as_view(), name='logout'),
    url(r'^registration/$', registration, name='account_registration'),
    url(r'^cart/$', show_cart, name='show_cart'),
    url(r'^ajax_add_to_cart/$', ajax_add_to_cart, name='ajax_add_to_cart'),
    url(r'^ajax_add_cart/$', ajax_add_to_cart, name='ajax_add_cart'),
    url(r'^get_message/(?P<pk>[-_\w]+)/$', login_required(get_messages), name='get_message'),
    url(r'^ajax_delete_to_cart/$', ajax_delete_to_cart, name='ajax_delete_to_cart'),
    url(r'^checkout_cart/$', login_required(checkout_cart), name='checkout_cart'),
    url(r'^ajax_plus_to_cart/$', ajax_plus_to_cart, name='ajax_plus_to_cart'),
    url(r'^ajax_minus_to_cart/$', ajax_minus_to_cart, name='ajax_minus_to_cart'),
    url(r'^dialogs/$', login_required(DialogsView.as_view(template_name='accounts/dialogs.html')), name='account_dialogs'),
    url(r'^chat/(?P<pk>[-_\w]+)/$', login_required(chat_view), name='chat'),
    url(r'^chat_control/(?P<u_pk>[-_\w]+)/$', login_required(chat_control_view), name='chat_control'),
    url(r'^public_chat/$', login_required(public_chat_view), name='public_chat'),
    url(r'^ajax_search_user/$', search_user_view, name='search_user'),
    url(r'^chat_add_user/(?P<pk>[-_\w]+)/(?P<u_pk>[-_\w]+)/$', chat_add_user_view, name='chat_add_user'),
    url(r'^set_chat_title/(?P<pk>[-_\w]+)/$', set_chat_title_view, name='set_chat_title'),
    url(r'^ajax_badge_cart/$', ajax_badge_cart, name='ajax_badge_cart'),
    url(r'^add_part/$', login_required(part_add), name='part_add'),
    url(r'^blog/(?P<u_pk>[-_\w]+)/$', login_required(post_list_view), name='blog_list'),
    url(r'^blog/(?P<slug>[-_\w]+)/$', login_required(post_detail_view), name='post_detail'),
    url(r'^blog_new/(?P<slug>[-_\w]+)/$', login_required(add_post_view), name='new_post'),
    url(r'^post_event/(?P<pk>[-_\w]+)/(?P<event>[-_\w]+)/$', login_required(post_event_view), name='post_event'),
    url(r'^comments/', include("django.contrib.comments.urls")),
    url(r'^part_delivery/', login_required(part_delivery), name='part_delivery'),
    url(r'^edit_data/(?P<data>[-_\w]+)/$', login_required(edit_data_view), name='edit_data'),
    url(r'^edit_address/(?P<pk>[-_\w]+)/$', login_required(edit_address_view), name='edit_address'),
    url(r'^delete_address/(?P<pk>[-_\w]+)/$', login_required(delete_address_view), name='delete_address'),
    url(r'^validation_cart/$', login_required(ajax_validation_cart), name='ajax_validation_cart'),
)
