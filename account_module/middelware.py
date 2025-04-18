from django.contrib import messages
from django.core.cache import cache
from django.shortcuts import redirect


class OTPRateLimitMiddleware:
    RATE_LIMIT = 5
    PERIOD = 180

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/accounts/login/' and request.method == 'POST':
            ip = self.get_client_ip(request)
            phone = request.POST.get('phone')
            if phone:
                key = f"otp_limit:{ip}:{phone}"
                request_count = cache.get(key, 0)

                if request_count >= self.RATE_LIMIT:
                    messages.error(request, "تعداد تلاش‌ها بیش از حد مجاز است. لطفاً بعداً امتحان کنید.")
                    return redirect('send_otp')

                else:
                    cache.set(key, request_count + 1, timeout=self.PERIOD)

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        if not request.user.is_authenticated and not request.path.startswith('/account_module/'):
            return redirect('account_module:login')
        return self.get_response(request)