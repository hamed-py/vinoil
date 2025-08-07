import phonenumbers
from django import forms
from utils.otp_phone import is_valid_phone


class PhoneField(forms.CharField):
    def to_python(self, value):
        value = super().to_python(value)
        try:
            p = phonenumbers.parse(value, 'IR')
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
            return phonenumbers.format_number(p, phonenumbers.PhoneNumberFormat.E164)
        except Exception:
            raise forms.ValidationError('شماره تلفن نامعتبر است.')


class RegisterForm(forms.Form):
    phone = PhoneField(
        label="",
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره تلفن',
                                      'lang': 'fa',
                                      'dir': 'rtl',
                                      })
    )
    new_password = forms.CharField(label= '',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور',
                                          'lang': 'fa',
                                          'dir': 'rtl',
                                          })
    )
    new_password_confirm = forms.CharField(label= '',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'تکرار رمز عبور',
                                          'lang': 'fa',
                                          'dir': 'rtl',
                                          })
    )

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('new_password')
        p2 = cleaned.get('new_password_confirm')
        if not p1 or not p2:
            raise forms.ValidationError('رمز عبور و تکرار آن باید وارد شود.')
        if p1 != p2:
            raise forms.ValidationError('رمزها مطابقت ندارند.')
        return cleaned


class LoginForm(forms.Form):
    phone = PhoneField(
        label="",
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره تلفن',
                                      'lang': 'fa',
                                      'dir': 'rtl', })
    )


class VerifyOTPForm(forms.Form):
    otp = forms.CharField(
        label="",
        min_length=6, max_length=6,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'کد تأیید',
                                      'lang': 'fa',
                                      'dir': 'rtl', })
    )


class ForgotPassForm(forms.Form):
    phone = PhoneField(
        label="",
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره تلفن',
                                      'lang': 'fa',
                                      'dir': 'rtl', })
    )


class ResetPassForm(forms.Form):
    otp = forms.CharField( label="",
        min_length=6, max_length=6,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'کد تأیید',
                                      'lang': 'fa',
                                      'dir': 'rtl',
                                      })
    )
    new_password = forms.CharField( label="",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز جدید',
                                          'lang': 'fa',
                                          'dir': 'rtl',
                                          })
    )
    new_password_confirm = forms.CharField( label="",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'تکرار رمز جدید',
                                          'lang': 'fa',
                                          'dir': 'rtl',
                                          })
    )

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('new_password') != cleaned.get('new_password_confirm'):
            raise forms.ValidationError('رمزها مطابقت ندارند.')
        return cleaned


class PhoneForm(forms.Form):
    phone = forms.CharField(
        max_length=15,
        label="",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'مثلاً 09121234567',
            'lang': 'fa',
            'dir': 'rtl',
        })
    )

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not is_valid_phone(phone):
            raise forms.ValidationError("شماره تماس معتبر نیست.")
        return phone


class OTPForm(forms.Form):
    otp = forms.CharField(
        label="",
        max_length=6,
        min_length=4,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'کد تأیید را وارد کنید',
            'lang': 'fa',
            'dir': 'rtl',
        })
    )

    def clean_otp(self):
        otp = self.cleaned_data.get('otp')
        if not otp.isdigit() or len(otp) != 6:
            raise forms.ValidationError("کد تأیید باید ۶ رقمی و فقط عدد باشد.")
        return otp
