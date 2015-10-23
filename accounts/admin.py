#coding: utf-8
from django.contrib import admin
from accounts.models import *
from catalog.models import *
from django import forms
from ckeditor.widgets import CKEditorWidget
from pytils.translit import slugify


class ProfileAdmin(admin.ModelAdmin):
    raw_id_fields = ['user']
    search_fields = ['phone']
    list_display = ('user', 'phone', 'sms_code')


class AddressAdmin(admin.ModelAdmin):
    search_fields = ['address']
    list_display = ('address', 'region', 'city', 'address_index', 'phones',)


class PartsInline(admin.TabularInline):
    raw_id_fields = ['part']
    model = PartsInShop
    extra = 1


class ShopAdmin(admin.ModelAdmin):
    raw_id_fields = ['profile', ]
    search_fields = ['phone']
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'profile',)
    inlines = (PartsInline,)


class ClientAdmin(admin.ModelAdmin):
    raw_id_fields = ['profile']
    search_fields = ['profile']
    list_display = ('profile',)


class ChatAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title',)


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Post
        fields = (
            'author',
            'title',
            'content',
            'is_public',
        )

    def save(self, commit=True):
        post = super(PostAdminForm, self).save(commit=False)
        post.slug = '%i-%s' % (
            Post.objects.last().pk+1, slugify(self.cleaned_data['title'])
        )
        post.save()
        return post


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    search_fields = ['title']
    list_display = ('pk', 'author', 'title', 'content', 'slug', 'is_public', 'ts_created', 'ts_changed', 'ts_public')
    raw_id_fields = ['author']


class PostCommentAdmin(admin.ModelAdmin):
    search_fields = ['text']
    list_display = ('post', 'user', 'answer_to', 'text', 'ts_created', 'is_public')

admin.site.register(Address, AddressAdmin)
admin.site.register(UserProfile, ProfileAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Chat, ChatAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostComment, PostCommentAdmin)

# Register your models here.
