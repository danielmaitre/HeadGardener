from django.conf import settings
from django.shortcuts import redirect


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            login_url = settings.LOGIN_URL
            if not request.path.startswith(login_url) and not request.path.startswith('/admin/'):
                return redirect(f'{login_url}?next={request.path}')
        return self.get_response(request)
