#coding: utf-8
from django import forms
from django.forms.widgets import RadioSelect
from accounts.models import *
from delivery.models import *


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address


class ShippingForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ('shipping',)
        widgets = {
            'shipping': RadioSelect,
        }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ('payment',)