from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from account_module.forms import RegisterForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from .models import User
from django.utils.crypto import get_random_string
from django.contrib.auth import login, logout
from utils.email_sevices import send_email


class RegisterViews(View):
    def get(self, request):
        register_form = RegisterForm()
        context = {
            'register_form': register_form,
        }
        return render(request, 'account_module/register.html', context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_email = register_form.cleaned_data['email']
            user_pass = register_form.cleaned_data['password']
            user: bool = User.objects.filter(email__iexact=user_email).exists()
            if user:
                register_form.add_error('email', 'این ایمیل قبلا در سایت ثبت نام کرده است')
            else:
                new_user = User(email=user_email, username=user_email, is_active=False,
                                email_active_code=get_random_string(72))
                new_user.set_password(user_pass)
                new_user.save()
                # todo send email active code
                send_email('فعالسازی حساب کاربری', new_user.email, {'user': new_user}, 'email/activate_account.html')
                return redirect(reverse('login_page'))

        context = {'register_form': register_form}
        return render(request, 'account_module/register.html', context)


class ActivateAccountView(View):
    def get(self, request, email_active_code):
        user: User = User.objects.filter(email_active_code__iexact=email_active_code).first()
        if user is not None:
            if not user.is_active:
                user.is_active = True
                user.email_active_code = get_random_string(72)
                user.save()
                send_email('فعالسازی حساب کاربری', user.email, {'user': user}, 'email/activate_account.html')
                return redirect(reverse('login_page'))
            else:
                pass
        raise Http404


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        context = {
            'login_form': login_form
        }

        return render(request, 'account_module/login_page.html', context)

    def post(self, request: HttpRequest):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data['email']
            user_pass = login_form.cleaned_data['password']
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                if not user.is_active:
                    login_form.add_error('email', 'حساب کاربری شما فعال نشده است')
                else:
                    is_pass_correct = user.check_password(user_pass)
                    if is_pass_correct:
                        login(request, user)
                        return redirect(reverse('home_page'))
                    else:
                        login_form.add_error('email', 'رمز عبور اشتباه است')
            else:
                login_form.add_error('email', 'کابری با مشخصات وارد شده یافت نشد')

        context = {
            'login_form': login_form
        }
        return render(request, 'account_module/login_page.html', context)


@method_decorator(login_required, name='dispatch')
class ForgotPasswordView(View):
    def get(self, request: HttpRequest):
        forget_password_form = ForgotPasswordForm()
        context = {
            'forget_password_form': forget_password_form
        }
        return render(request, 'account_module/forgot_pass.html', context)

    def post(self, request: HttpRequest):
        forget_password_form = ForgotPasswordForm(request.POST)
        if forget_password_form.is_valid():
            user_email = forget_password_form.cleaned_data['email']
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                send_email('بازیابی کلمه عبور', user.email, {'user': user}, 'email/forgot_password.html')
                return redirect(reverse('home_page'))


@method_decorator(login_required, name='dispatch')
class ResetPasswordView(View):
    def get(self, request: HttpRequest, active_code):
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if user is None:
            return redirect(reverse('login_page'))

        reset_password_form = ResetPasswordForm()
        context = {
            'reset_password_form': reset_password_form,
            'user': user
        }

        return render(request, 'account_module/reset_pass.html', context)

    def post(self, request: HttpRequest, active_code):
        reset_password_form = ResetPasswordForm(request.POST)
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if reset_password_form.is_valid():
            if user is None:
                return redirect(reverse('login_page'))
            user_new_pass = reset_password_form.cleaned_data.get('password')
            user.set_password(user_new_pass)
            user.email_active_code = get_random_string(72)
            user.is_active = True
            user.save()
            return redirect(reverse('login_page'))

        context = {
            'reset_password_form': reset_password_form,
            'user': user
        }

        return render(request, 'account_module/reset_pass.html', context)


@method_decorator(login_required, name='dispatch')
class LogOutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('login_page'))
