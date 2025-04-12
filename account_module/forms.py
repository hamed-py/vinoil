from django import forms
from django.core import validators
from django.utils.log import RequireDebugFalse


class RegisterForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ایمیل'
        }),
        validators=[
            validators.EmailValidator(),
            validators.MaxLengthValidator(64)
        ],
        error_messages={
            'invalid': 'لطفا یک ایمیل معتبر وارد کنید!'
        }
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور'
        }),
        validators=[
            validators.MaxLengthValidator(20),
            validators.MinLengthValidator(4),

        ]
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'تکرار رمز عبور'
        }),
        validators=[
            validators.MaxLengthValidator(20),
            validators.MinLengthValidator(4),
        ]
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'رمز عبور و تکرار رمز عبور باهم مغایرت دارند')

        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ایمیل',

        }),
        validators=[
            validators.EmailValidator(),
            validators.MaxLengthValidator(64),
        ]
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور ',
        }),
        validators=[
            validators.MaxLengthValidator(20),
            validators.MinLengthValidator(4),

        ]
    )


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'لطفا ایمیل خود را وارد کنید'
        }),
        validators=[
            validators.EmailValidator(),
            validators.MaxLengthValidator(64),
        ]
    )


class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور جدید',
        }),
        validators=[
            validators.MaxLengthValidator(20),
            validators.MinLengthValidator(4),
        ]
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'تکرار رمز عبور جدید'

        }),
        validators=[
            validators.MaxLengthValidator(20),
            validators.MinLengthValidator(4),
        ]
    )