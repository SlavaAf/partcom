#coding: utf-8

from django.db import models
from accounts.models import *
from django.core.exceptions import ValidationError

TYPE_CHOICES = (
    (0, u'Новый'),
    (1, u'Б\У'),
)


class Part(models.Model):
    article = models.CharField(verbose_name='Артикул', max_length=100, default='', null=False, blank=False)
    slug = models.SlugField(verbose_name='Ссылка', unique=False, db_index=True)
    title = models.CharField(verbose_name='Наименование', max_length=100, default='', null=False)

    class Meta:
        verbose_name = 'Запчасть'
        verbose_name_plural = 'Запчасти'

    def __unicode__(self):
        return u'{0} ({1})'.format(self.title, self.article)


class PartsInShop(models.Model):
    part = models.ForeignKey(Part, related_name='ps_parts', verbose_name='Запчасть')
    shop = models.ForeignKey('accounts.Shop', related_name='ps_shops', verbose_name='Магазин')
    count = models.IntegerField(verbose_name='Количество', max_length=100, default=0)
    price = models.DecimalField(verbose_name='Стоимость', max_digits=9, decimal_places=2)
    type = models.IntegerField(verbose_name='Тип', max_length=1, choices=TYPE_CHOICES, default=0)

    class Meta:
        verbose_name = u'Запчасть а магазине'
        verbose_name_plural = u'Запчасти в магазине'

    def __unicode__(self):
        return u'{0} ({1} {2})'.format(self.shop, self.part, self.type)
