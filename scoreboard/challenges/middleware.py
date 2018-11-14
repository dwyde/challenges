from django.conf import settings
from django.contrib.auth import login, get_user_model


class AuthenticationMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            model = get_user_model()
            user = model.objects.create_user()
            login(request, user)

        response = self.get_response(request)
        return response
