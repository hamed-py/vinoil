import os
from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from  django.utils.text import slugify
from account_module.models import User


class EditProfileModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'address', 'phone', 'about_user', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام',
                'id': 'name',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام خانوادگی',
                'id': 'subject',
                'name': 'subject',
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'آدرس',
                'rows': '4',
                'id': 'message',

            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',

            }),
            'about_user': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'درباره من',
                'rows': '4',
            }),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),

        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            name, ext = os.path.splitext(avatar.name)

            name = name.replace('.png', '').replace('.jpg', '')

            avatar.name = f"{slugify(name)}{ext.lower()}"
        return avatar


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(label='رمز عبور فعلی', widget=forms.PasswordInput(attrs={
        'class': 'form-control',

    }),
                                       validators=[
                                           validators.MaxLengthValidator(100),
                                       ])
    password = forms.CharField(label='رمز عبور جدید', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
    }),
                               validators=[
                                   validators.MaxLengthValidator(100),
                                   validators.MinLengthValidator(4),
                               ])
    confirm_password = forms.CharField(label='تکرار رمز عبور جدید', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
    }),
                                       validators=[
                                           validators.MaxLengthValidator(100),
                                           validators.MinLengthValidator(4),
                                       ])

    def clean_new_password(self):
        new_password = self.cleaned_data.get('password')
        confirm_new_password = self.cleaned_data.get('confirm_password')
        if new_password == confirm_new_password:
            return confirm_new_password

        raise ValidationError('رمز عبور جدید و تکرار آن باهم مغایرت دارند!')
