from functools import wraps

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect


def group_required(*group_name):
    """
    Декоратор для проверки принадлежности пользователя к указанной группе.
    Если пользователь не входит в группу, перенаправляет на страницу входа.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            print(request.user.groups.all().filter(name__in=group_name).exists())
            if request.user.groups.all().filter(name__in=group_name).exists():
                return view_func(request, *args, **kwargs)
            else:
                return view_func(request, *args, **kwargs)
                # Здесь можно указать любую страницу, куда вы хотите перенаправлять пользователей,
                # return redirect('/')
        return wrapper
    return decorator

def anonymous_required(function=None, redirect_url=None):
   if not redirect_url:
       redirect_url = settings.LOGIN_REDIRECT_URL
   actual_decorator = user_passes_test(
       lambda u: u.is_anonymous(),
       login_url=redirect_url
   )
   if function:
       return actual_decorator(function)
   return actual_decorator
