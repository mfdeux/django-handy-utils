import json
from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import exception_handler


def error_404_view(request, exception=None):
    response = {'status_code': 404, 'error': 'The resource was not found'}
    return HttpResponse(json.dumps(response), content_type='application/json', status=status.HTTP_404_NOT_FOUND)


def error_500_view(request, exception=None):
    response = {'status_code': 500, 'error': 'Internal server error'}
    return HttpResponse(json.dumps(response), content_type='application/json',
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        # check if exception has dict items
        if hasattr(exc.detail, 'items'):
            # remove the initial value
            response.data = {}
            errors = []
            for key, value in exc.detail.items():
                # append errors into the list
                errors.append("{} : {}".format(key, " ".join(value)))

            # add property errors to the response
            response.data['errors'] = errors

        # serve status code in the response
        response.data['status_code'] = response.status_code

    return response