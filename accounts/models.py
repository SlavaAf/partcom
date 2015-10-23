#coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from catalog.models import *
from datetime import datetime

COUNTRY_CHOICES = (
    ('KZ', 'Казахстан'),
)

REGION_CHOICES = (
    ('VKO', 'Восточно-Казахстанская область'),
)

CITY_CHOICES = (
    ('UKG', 'Усть-Каменогорск'),
)


class Address(models.Model):
    country = models.CharField(verbose_name='Страна', max_length=3, choices=COUNTRY_CHOICES, default='KZ')
    region = models.CharField(verbose_name='Область', max_length=4, choices=REGION_CHOICES, default='VKO')
    city = models.CharField(verbose_name='Город', max_length=100, choices=CITY_CHOICES, default='UKG')
    address = models.CharField(verbose_name='Адрес', max_length=100)
    address_index = models.CharField(verbose_name='Индекс', max_length=10, default='070000')
    phones = models.CharField(verbose_name='Телефоны', max_length=100, default='')
    details = models.CharField(verbose_name='Примечания', max_length=1000, null=True, blank=True, default='')

    class Meta:
        verbose_name = 'адрес'
        verbose_name_plural = 'адреса'
        ordering = ['country', 'region', 'city', 'address', 'pk']

    def __unicode__(self):
        return self.address


ACCOUNT_TYPES = (
    (1, u'Покупатель'),
    (2, u'Продавец'),
)


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', verbose_name='Профиль')
    addresses = models.ManyToManyField(Address, related_name='profiles', verbose_name='Адреса', null=True)
    phone = models.CharField(verbose_name='Телефон', max_length=100, unique=True)
    sms_code = models.CharField(verbose_name='СМС код', max_length=100, default=0)
    account_type = models.IntegerField(verbose_name='Тип аккаунта', default=1, choices=ACCOUNT_TYPES)

    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'

    def __unicode__(self):
        return self.user.username

    @property
    def email(self):
        return self.user.email

    def get_chats_with_user(self, user):
        chats = self.chats.select_related().filter(users=user)
        for c in chats:
            if c.users.count() == 2:
                return c
        return False

    def get_permissions_for_chat(self, chat_pk):
        if self.chats.filter(pk=chat_pk): return True
        else: return False

    def get_fullname(self):
        if self.shop.all():
            return self.shop.get().title
        else:
            return self.user.get_full_name()


class Shop(models.Model):
    profile = models.ForeignKey(UserProfile, related_name='shop', verbose_name='Профиль')
    title = models.CharField(verbose_name=u'Наименование', max_length=100, unique=True)
    slug = models.SlugField(verbose_name='Ссылка', unique=True, default='')
    parts = models.ManyToManyField('catalog.Part', related_name='shops', through='catalog.PartsInShop',
                                   verbose_name='Запчасти')

    def __unicode__(self):
        return u'{0}'.format(self.title)

    class Meta:
        verbose_name = 'магазин'
        verbose_name_plural = 'магазины'


class Client(models.Model):
    profile = models.ForeignKey(UserProfile, related_name='client', verbose_name='Профиль')

    def __unicode__(self):
        return u'{0}'.format(self.profile)

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Chat(models.Model):
    users = models.ManyToManyField(UserProfile, related_name='chats', verbose_name='Собеседники')
    title = models.CharField(verbose_name='Тема', max_length=100, null=True, blank=True, default='')

    def __unicode__(self):
        return u'{0}'.format(self.pk)

    def get_channel_name(self):
        return 'channel'+self.pk

    class Meta:
        verbose_name = 'чат'
        verbose_name_plural = 'чаты'


class Post(models.Model):
    author = models.ForeignKey(UserProfile, related_name='posts', verbose_name='автор')
    title = models.CharField(verbose_name='Тема', max_length=255)
    ts_created = models.DateTimeField(verbose_name='Дата создания', default=datetime.now(), auto_now_add=True)
    ts_changed = models.DateTimeField(verbose_name='Дата изменения', default=datetime.now(), auto_now=True, auto_now_add=True)
    ts_public = models.DateTimeField(verbose_name='Дата публикации', null=True, blank=True)
    content = models.TextField(verbose_name='Текст', max_length=10000)
    is_public = models.BooleanField(verbose_name='Статус публикации', default=False)
    slug = models.SlugField(verbose_name='Ссылка', default='', max_length=160)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/blogs/"+str(self.author.pk)+"/" + self.slug

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'


class PostComment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', verbose_name='Пост')
    ts_created = models.DateTimeField(verbose_name='Дата создания', default=datetime.now(), auto_now_add=True)
    user = models.ForeignKey(UserProfile, related_name='post_comments', verbose_name='Адресант')
    answer_to = models.ForeignKey('self', related_name='post_answers',  null=True, blank=True, verbose_name='Адресат')
    text = models.CharField(verbose_name='Текст', max_length=10000)
    is_public = models.BooleanField(verbose_name='Статус публикации', default=True)

    def __unicode__(self):
        return self.text

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
        ordering = ['ts_created']