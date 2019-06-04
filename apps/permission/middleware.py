from django.shortcuts import render,HttpResponse
from django.utils.deprecation import MiddlewareMixin
import requests
import json


class HttpResponseAuthenticationFailed(HttpResponse):
    status_code = 401

class TokenMiddleware(MiddlewareMixin):

    def process_request(self, request):
        try:
            Authorization = request.headers["Authorization"]
            if Authorization:
                headers = {"Authorization": Authorization}
                r = requests.get("http://101.200.61.189:52131/userInfo/", headers=headers)
                if r.status_code == 200:
                    request.user = r.json()
                    print(type(request.user))
                else:
                    content = {"detail": "Authentication credentials were not provided."}
                    return HttpResponseAuthenticationFailed(json.dumps(content))
        except Exception as e:
            pass





