#coding: utf-8
from django.db import models
from catalog.models import *
from accounts.models import *


TYPE_CHOICES = (
    ('ts_accept', 'В обработке'),
    ('ts_buy', 'Оплаченный'),
    ('ts_ended', 'Завершенный'),
    ('ts_created', 'В ожидании'),
)


SHIP_CHOICES = (
    ('td_pickup', 'Самовывоз'),
    ('td_courier', 'Курьерская доставка'),
)


PAY_CHOICES = (
    ('tp_cash', 'Наличный расчет'),
    ('tp_card', 'Оплата банковской картой'),
    ('tp_direct', 'Прямой перевод'),
)


STATE_CHOICES = (
    ('pd_created', 'В обработке'),
    ('pd_ship', 'Готов к отправке'),
    ('pd_fail', 'Отказано'),
)


class Delivery(models.Model):
    parts_in_del = models.ManyToManyField('catalog.PartsInShop', related_name='dd_parts', through='delivery.PartInDelivery', verbose_name=u'Запчасть')
    client_del = models.ForeignKey('accounts.UserProfile', verbose_name=u'Клиент', related_name='dd_client', null=True, blank=False, default=None)
    payment = models.CharField(verbose_name=u'Оплата', max_length=10, choices=PAY_CHOICES, default=0)
    shipping = models.CharField(verbose_name=u'Доставка', max_length=10, choices=SHIP_CHOICES, default=0)
    state = models.CharField(verbose_name=u'Статус', max_length=10, choices=TYPE_CHOICES)
    amount = models.DecimalField(verbose_name=u'Стоимость', max_digits=9, decimal_places=2, default=0)
    address = models.ForeignKey('accounts.Address', related_name='d_address', verbose_name=u'Адрес доставки', null=True, blank=True, default=None)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __unicode__(self):
        return u'{0}'.format(self.client_del)


class PartInDelivery(models.Model):
    part_del = models.ForeignKey('delivery.Delivery', related_name='ps_del', verbose_name='Заказ', blank=True, null=True, default=None)
    part_in_shop = models.ForeignKey('catalog.PartsInShop', related_name='ps_part_in_del', blank=True, null=True, default=None, verbose_name='Запчасть в заказе')
    quantity = models.IntegerField(verbose_name=u'Количество', max_length=100, default=0)
    del_in_shop = models.ManyToManyField('accounts.Shop', related_name='pd_dis', blank=True, null=True, default=None, verbose_name='Заказ на запчасть в магазине')
    state_in_part = models.CharField(verbose_name='Статус запчасти', max_length=15, choices=STATE_CHOICES)


    class Meta:
        verbose_name = u'Запчасть в заказе'
        verbose_name_plural = u'Запчасти в заказе'

    def __unicode__(self):
        return u'{0}'.format(self.quantity)