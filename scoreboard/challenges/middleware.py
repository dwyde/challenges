from django.conf import settings
from django.contrib.auth import authenticate, login


class AuthenticationMiddleware(object):
    # FIXME: automatically log in as a default user.

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated():
            user = authenticate(username=settings.DEFAULT_USERNAME,
                                password=settings.DEFAULT_PASSWORD)
            login(request, user)

        response = self.get_response(request)
        return response
