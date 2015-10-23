from django.conf.urls import *

from django.contrib import admin
from accounts.views import SSE, PostsListView, post_detail_view, post_list_view, index_view


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', index_view, name='index'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^catalog/', include('catalog.urls')),
    url(r'^account/', include('accounts.urls')),
    url(r'^sse/(?P<channel>\w+)/$', SSE.as_view(redis_channel='main_channel'), name='sse_main_channel'),
    url(r'^blogs/$', PostsListView.as_view(), name='blogs_list'),
    url(r'^blogs/(?P<u_pk>[-_\w]+)/(?P<slug>[-_\w]+)/$', post_detail_view, name='posts_detail'),
    url(r'^blogs/(?P<u_pk>[-_\w]+)/$', post_list_view, name='user_blog'),
    url(r'^ckeditor/', include('ckeditor.urls')),
)
