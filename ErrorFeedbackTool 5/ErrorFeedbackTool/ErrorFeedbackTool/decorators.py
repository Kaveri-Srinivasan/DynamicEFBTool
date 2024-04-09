from django.shortcuts import redirect

def restrict_direct_access(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.META.get('HTTP_REFERER'):
            return redirect('login')  
        return view_func(request, *args, **kwargs)
    return wrapper
