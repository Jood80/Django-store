import json

from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.http import require_POST
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


def get_csrf(request):
    response = JsonResponse({'info': 'Success - Set CSRF cookie'})
    response['X-CSRFToken'] = get_token(request)
    return response


@require_POST
def login_view(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    if username is None or password is None:
        return JsonResponse({'info': 'username & password are required!'})

    user = authenticate(username=username, password=password)

    if user is None:
        return JsonResponse({'info': 'User does not exist'}, status=400)

    login(request, user)
    return JsonResponse({'info': 'logged in successfully'})


class WhoAmIView(APIView):
    authentication_classes = [SessionAuthentication]
    Permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, format=None):
        print(request.user.username)
        return JsonResponse({'username', request.user.username})
