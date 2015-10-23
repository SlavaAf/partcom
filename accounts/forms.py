# -*- coding: utf-8 -*-
from django import forms
import re
from django.contrib.auth.models import User
from accounts.models import ACCOUNT_TYPES, Address, Shop
from ckeditor.widgets import CKEditorWidget


class AuthSendSmsForm(forms.Form):
    phone = forms.CharField(label=u'Номер телефона', max_length=12)

    def clean_phone(self):
        number = self.cleaned_data['phone']
        raw_number = re.sub('[^0-9]', u'', str(number.encode('utf-8')))
        if len(raw_number) < 10 or len(raw_number) > 11:
            raise forms.ValidationError(u'Неверный формат номера телефона')
        elif len(raw_number) == 11:
            if raw_number.startswith('8') or raw_number.startswith('7'):
                raw_number = raw_number[1:]
        return '7' + raw_number


class AuthRegistrationForm(forms.Form):
    email = forms.EmailField(label=u'Email', max_length=100)
    first_name = forms.CharField(label=u'Имя', max_length=100)
    last_name = forms.CharField(label=u'Фамилия', max_length=100)
    account_type = forms.ChoiceField(label=u'Тип аккаунта', choices=ACCOUNT_TYPES, help_text=u'Покупатель может только покупать, а продавец покупать и продавать.')


class AuthInputCodeForm(forms.Form):
    code = forms.CharField(label=u'Полученный код', max_length=100)


class DialogsForm(forms.Form):
    message = forms.CharField(label=u'Сообщение', max_length=10000)


class AddPartForm(forms.Form):
    article = forms.CharField(label=u'Артикул', max_length=100)
    title = forms.CharField(label=u'Наименование', max_length=100)
    price = forms.IntegerField(label=u'Стоимость', max_value=100000)
    count = forms.IntegerField(label=u'Колличество', max_value=100000)
    type = forms.CheckboxInput()


class AddPostForm(forms.Form):
    title = forms.CharField(label='Тема', max_length=255)
    content = forms.CharField(widget=CKEditorWidget(), label='Текст', max_length=10000)


class StatePartDelForm(forms.Form):
    accept = forms.CheckboxInput()


class EditUserDataForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
        error_messages = {
            'email': {
                'invalid': "Некорректный адрес электронной почты.",
            },
        }


class EditAddressesDataForm(forms.ModelForm):
    class Meta:
        model = Address


class EditShopDataForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['title',]