from functools import wraps

# module imported by Widya
from django.shortcuts import render


def xframe_options_deny(view_func):
    """
    Modify a view function so its response has the X-Frame-Options HTTP
    header set to 'DENY' as long as the response doesn't already have that
    header set. Usage:

    @xframe_options_deny
    def some_view(request):
        ...
    """

    """----------------------------------------------
        Modified by widya - added attribute forbid_site and original request (httprequestadd) to throw forbidden template in view function
        wrapped by xframe_options_deny
    """#----------------------------------------------
    def wrapped_view(*args, **kwargs):
        resp = view_func(*args, **kwargs)
        if resp.get('X-Frame-Options') is None:
            if hasattr(resp, 'forbid_site'):
                resp = render(resp.httprequestadd, resp.forbid_site)
                resp['X-Frame-Options'] = 'SAMEORIGIN'
        return resp
    return wraps(view_func)(wrapped_view)


def xframe_options_sameorigin(view_func):
    """
    Modify a view function so its response has the X-Frame-Options HTTP
    header set to 'SAMEORIGIN' as long as the response doesn't already have
    that header set. Usage:

    @xframe_options_sameorigin
    def some_view(request):
        ...
    """
    def wrapped_view(*args, **kwargs):
        resp = view_func(*args, **kwargs)
        if resp.get('X-Frame-Options') is None:
            resp['X-Frame-Options'] = 'SAMEORIGIN'
        return resp
    return wraps(view_func)(wrapped_view)


def xframe_options_exempt(view_func):
    """
    Modify a view function by setting a response variable that instructs
    XFrameOptionsMiddleware to NOT set the X-Frame-Options HTTP header. Usage:

    @xframe_options_exempt
    def some_view(request):
        ...
    """
    def wrapped_view(*args, **kwargs):
        resp = view_func(*args, **kwargs)
        resp.xframe_options_exempt = True
        return resp
    return wraps(view_func)(wrapped_view)
