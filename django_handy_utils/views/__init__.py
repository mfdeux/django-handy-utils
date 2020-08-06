from django.http import HttpResponse
from django.http.request import HttpRequest


def healthcheck_view(request: HttpRequest):
    """
    Healthcheck view returning an empty 200 response
    """
    return HttpResponse('')
