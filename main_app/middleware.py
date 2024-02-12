from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.shortcuts import redirect
from vendor_management_system.settings import DB

class LoginCheckMiddleWare(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        # session_id = request.META.get('HTTP_COOKIE', {}).split('sessionid=')[1]
        # session_data = DB.session.find({'session_id': session_id, 'is_active': True})
        # if session_data:
        #     return redirect("/")
        # else:
        #     if request.path == reverse('login'):
        #         return redirect('login')
        #     else:
        #         return redirect('login')
