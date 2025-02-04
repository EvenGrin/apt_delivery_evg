# middleware.py
import re

from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings


class RedirectIfAuthenticatedMiddleware(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        excluded_paths = getattr(settings, 'REDIRECT_AUTHENTICATED_EXCLUDE', [])

        if request.user.is_authenticated:
            user = request.user
            if not any(
                    request.path.startswith(pattern)
                    for pattern in excluded_paths
            ):
                if request.path.startswith('/accounts/login') or request.path.startswith('/accounts/registration'):
                    return redirect(reverse('home'))
                if user.is_superuser:
                    if not request.path.startswith('/admin'):
                        # return redirect(reverse('home'))
                        return redirect(reverse('admin:index'))
                if user.groups.filter(name='operator').exists():
                    if not request.path.startswith('/admin'):
                        # return redirect(reverse('home'))
                        return redirect(reverse('admin:index'))
                if user.groups.filter(name='deliver').exists():
                    if not request.path.startswith('/deliver'):
                        return redirect(reverse('deliver'))
