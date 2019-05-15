import requests

from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def login(request):
    data = request.data
    username = data.get('username', None)
    password = data.get('password', None)

    user = authenticate(username=username, password=password)

    if user:
        data = {'grant_type':'password',
                'provision_key':settings.PROVISION_KEY,
                'authenticated_userid':user.id,
                'client_id':settings.CLIENT_ID,
                'client_secret':settings.CLIENT_SECRET,
                }
        response = requests.post('https://dev.inetcop.org:8443/api/static/oauth2/token', data)
        if response.status_code == 200:
            return Response(status=200, data=response.json())
    else:
        return Response(status=400)

@api_view(['POST'])
def refresh_token(request):
    data = request.data
    refresh_token = data.get('refresh_token')
    if refresh_token:
        data = {
            'grant_type': 'refresh_token',
            'client_id': settings.CLIENT_ID,
            'client_secret': settings.CLIENT_SECRET,
            'refresh_token': refresh_token
        }
        response = requests.post('https://dev.inetcop.org:8443/api/static/oauth2/token', data)
        if response.status_code == 200:
            return Response(status=200, data=response.json())
    else:
        return Response(status=400)
