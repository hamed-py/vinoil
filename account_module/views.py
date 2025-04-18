from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout, get_user_model
from django.urls import reverse
from django.contrib import messages
from django.core.cache import cache
from django.utils.safestring import mark_safe
from .forms import (RegisterForm, LoginForm, VerifyOTPForm,
                    ForgotPassForm, ResetPassForm)
from .sms import send_sms_code, verify_sms_code
from .models import AuthLog

User = get_user_model()
FAILED_LIMIT = 5
LOCKOUT_TTL = 15 * 60

class BaseOTPView:
    def log_event(self, phone, event, success):
        AuthLog.objects.create(phone=phone, event=event, success=success)

class RegisterView(BaseOTPView, View):
    def get(self, req):
        return render(req, 'account_module/register.html', {'form': RegisterForm()})

    def post(self, req):
        form = RegisterForm(req.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            if User.objects.filter(phone=phone).exists():
                # افزودن خطا با لینک به ورود
                url = reverse('account_module:login')
                form.add_error(
                    'phone',
                    mark_safe(f'این شماره قبلاً ثبت شده است. برای ورود <a href="{url}">اینجا</a> کلیک کنید.')
                )
                return render(req, 'account_module/register.html', {'form': form})
            # ذخیره موقت رمز در session
            req.session['register_data'] = {
                'phone': phone,
                'password': form.cleaned_data['new_password']
            }
            try:
                send_sms_code(phone)
                return redirect('account_module:verify_otp')
            except Exception as e:
                form.add_error(None, str(e))
        return render(req, 'account_module/register.html', {'form': form})

class LoginView(BaseOTPView, View):
    def get(self, req):
        return render(req, 'account_module/login_page.html', {'form': LoginForm()})

    def post(self, req):
        form = LoginForm(req.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            if not User.objects.filter(phone=phone).exists():
                messages.error(req, mark_safe('شماره ثبت نشده است. برای ثبت‌نام <a href="'+
                      reverse('account_module:register')+'">اینجا</a> کلیک کنید.'))
                return redirect('account_module:register')
            try:
                send_sms_code(phone)
                req.session['login_phone'] = phone
                return redirect('account_module:verify_otp')
            except Exception as e:
                form.add_error(None, str(e))
        return render(req, 'account_module/login_page.html', {'form': form})

class VerifyOTPView(BaseOTPView, View):
    def get(self, req):
        data = req.session.get('register_data') or {'phone': req.session.get('login_phone')}
        return render(req, 'account_module/verify.html', {
            'form': VerifyOTPForm(),
            'pending_phone': data.get('phone')
        })

    def post(self, req):
        form = VerifyOTPForm(req.POST)
        reg = req.session.get('register_data')
        phone = (reg or {}).get('phone') or req.session.get('login_phone')
        if not phone:
            return redirect('account_module:login')
        if cache.get(f"lockout_{phone}"):
            messages.error(req, 'حساب قفل است. بعداً تلاش کنید.')
            return redirect('account_module:verify_otp')
        if form.is_valid():
            if verify_sms_code(phone, form.cleaned_data['otp']):
                # ثبت یا ورود
                if reg:
                    # ثبت‌نام
                    User.objects.create_user(
                        phone=phone,
                        password=reg['password']
                    )
                    del req.session['register_data']
                user = User.objects.get(phone=phone)
                login(req, user)
                self.log_event(phone, 'register' if reg else 'login', True)
                # پاک‌سازی session های شماره
                req.session.pop('login_phone', None)
                return redirect('home_page')
            # خطای OTP
            cnt = cache.get(f"fail_{phone}", 0) + 1
            cache.set(f"fail_{phone}", cnt, LOCKOUT_TTL)
            if cnt >= FAILED_LIMIT:
                cache.set(f"lockout_{phone}", True, LOCKOUT_TTL)
                messages.error(req, 'تعداد تلاش‌ها زیاد شد و حساب قفل شد.')
            else:
                messages.error(req, 'کد نادرست است.')
        return render(req, 'account_module/verify.html', {'form': form, 'pending_phone': phone})

class ResendOTPView(BaseOTPView, View):
    def get(self, req):
        if req.session.get('register_data'):
            phone = req.session['register_data']['phone']
        else:
            phone = req.session.get('login_phone') or req.session.get('phone_reset')
        try:
            send_sms_code(phone)
            messages.success(req, 'کد مجدد ارسال شد.')
        except Exception as e:
            messages.error(req, str(e))
        # بازگشت
        return redirect('account_module:verify_otp')

class LogoutView(View):
    def get(self, req):
        logout(req)
        return redirect('account_module:login')

class ForgotPasswordView(BaseOTPView, View):
    def get(self, req):
        return render(req, 'account_module/forgot_pass.html', {'form': ForgotPassForm()})
    def post(self, req):
        form = ForgotPassForm(req.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            if not User.objects.filter(phone=phone).exists():
                form.add_error('phone', 'شماره ثبت نشده است.')
            else:
                try:
                    send_sms_code(phone)
                    req.session['phone_reset'] = phone
                    return redirect('account_module:reset_password')
                except Exception as e:
                    form.add_error(None, str(e))
        return render(req, 'account_module/forgot_pass.html', {'form': form})

class ResetPasswordView(BaseOTPView, View):
    def get(self, req):
        return render(req, 'account_module/reset_pass.html', {'form': ResetPassForm()})
    def post(self, req):
        form = ResetPassForm(req.POST)
        phone = req.session.get('phone_reset')
        if not phone:
            return redirect('account_module:forgot_password')
        if form.is_valid() and verify_sms_code(phone, form.cleaned_data['otp']):
            user = User.objects.get(phone=phone)
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            del req.session['phone_reset']
            self.log_event(phone, 'reset', True)
            messages.success(req, 'رمز عبور با موفقیت تغییر یافت.')
            return redirect('account_module:login')
        if form.errors:
            messages.error(req, form.errors.as_text())
        return render(req, 'account_module/reset_pass.html', {'form': form})