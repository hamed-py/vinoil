from django.test import TestCase, Client
from django.urls import reverse
from django.core.cache import cache
from .models import User

class AccountModuleTests(TestCase):
    def setUp(self):
        self.client = Client()
        cache.clear()
        self.phone = '+989120000000'

    def test_full_register_verify_flow(self):
        resp = self.client.post(reverse('account_module:register'), {'phone': self.phone})
        self.assertRedirects(resp, reverse('account_module:verify_otp'))
        code = cache.get(f"otp_{self.phone}")
        resp = self.client.post(reverse('account_module:verify_otp'), {'otp': code})
        self.assertRedirects(resp, '/')
        self.assertTrue(User.objects.filter(phone=self.phone).exists())

    def test_resend_otp(self):
        self.client.post(reverse('account_module:register'), {'phone': self.phone})
        old = cache.get(f"otp_{self.phone}")
        resp = self.client.get(reverse('account_module:resend_otp'))
        new = cache.get(f"otp_{self.phone}")
        self.assertNotEqual(old, new)

    def test_login_via_otp(self):
        # درخواست OTP
        resp = self.client.post(reverse('account_module:login'), {'phone': self.phone})
        self.assertRedirects(resp, reverse('account_module:verify_otp'))
        code = cache.get(f"otp_{self.phone}")
        # پس از verify در همان view login
        resp = self.client.post(reverse('account_module:login'), {'phone': self.phone, 'otp': code})
        self.assertRedirects(resp, '/')

    def test_forgot_reset_password(self):
        User.objects.create_user(phone=self.phone, password='oldpass')
        resp = self.client.post(reverse('account_module:forgot_password'), {'phone': self.phone})
        self.assertRedirects(resp, reverse('account_module:reset_password'))
        code = cache.get(f"otp_{self.phone}")
        resp = self.client.post(reverse('account_module:reset_password'), {
            'otp': code,
            'new_password': 'newpass123',
            'new_password_confirm': 'newpass123'
        })
        self.assertRedirects(resp, reverse('account_module:login'))
        user = User.objects.get(phone=self.phone)
        self.assertTrue(user.check_password('newpass123'))