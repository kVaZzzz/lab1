from django import forms
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from .models import *


class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(label='Логин', validators=[
        RegexValidator('^[a-zA-Z-]+$', message='Разрешены только латиница и дефис')], error_messages={
        'required': 'Обязательное поле',
        'unique': 'Данный логин занят'
    })
    email = forms.EmailField(label='Почта', error_messages={
        'invalid': 'Не правильный формат адреса почты',
        'unique': 'Данная почта занята'
    })
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput, error_messages={
        'required': 'Обязательное поле'
    })
    password2 = forms.CharField(label='Пароль повторно', widget=forms.PasswordInput, error_messages={
        'required': 'Обязательное поле'
    })
    name = forms.CharField(label='Имя', validators=[
        RegexValidator('^[а-яА-Я- ]+$', message='В поле имя может быть только кириллица, дефис или пробел')],
                            error_messages={'required': 'Обязательное поле'})

    last_name = forms.CharField(label='Фамилия', validators=[
        RegexValidator('^[а-яА-Я- ]+$', message='В поле фамилия может быть только кириллица, дефис или пробел')],
                            error_messages={'required': 'Обязательное поле'})

    surname = forms.CharField(label='Отчество', validators=[
        RegexValidator('^[а-яА-Я- ]+$', message='В поле отчество может быть только кириллица, дефис или пробел')],
                            error_messages={'required': 'Обязательное поле'})

    personal_data = forms.BooleanField(required=True, label='Согласие на обработку персональных данных',
                                       error_messages={'required': 'Обязательное поле'})
    avatar = forms.ImageField(label='Аватар', required=False)

    def clean(self):
        super().clean()
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise ValidationError({
                'password2': ValidationError('Введенные пароли не совпадают', code='password_missmatch')
            })

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data["password"]
        if password:
            user.password = make_password(password)
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'name', 'last_name', 'surname', 'personal_data', 'avatar')

class UserForm(forms.ModelForm):

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data["password"]
        if password:
            user.password = make_password(password)
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['name', 'surname', 'username', 'email', 'password', 'avatar']


class VoteForm(forms.Form):
    name = forms.CharField(max_length=100, label='Название опроса')
    content = forms.CharField(max_length=2000, widget=forms.Textarea(), label='Описание опроса')
    photo = forms.ImageField(label='Фото для опроса')
    choice1 = forms.CharField(max_length=100, label='Вариант 1')
    choice2 = forms.CharField(max_length=100, label='Вариант 2')
    choice3 = forms.CharField(max_length=100, label='Вариант 3')