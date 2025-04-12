from django import forms
from .models import Contact_Us


class ContactUsModelForm(forms.ModelForm):
    class Meta:
        model = Contact_Us
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام و نام خانوادگی',
                'id': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ایمیل',
                'id': 'email',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'موضوع',
                'id': 'subject',
                'name': 'subject',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'متن پیام',
                'rows': '5',
                'id': 'message',

            }),
        }




