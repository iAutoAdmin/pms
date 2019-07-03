from django.http import HttpResponse, JsonResponse
from django.utils.deprecation import MiddlewareMixin
import requests
import json


class HttpResponseAuthenticationFailed(HttpResponse):
    status_code = 401


class TokenMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.path != "/docs/":
            try:
                Authorization = request.headers["Authorization"]
                if Authorization:
                    headers = {"Authorization": Authorization}
                    r = requests.get("http://101.200.61.189:52131/userInfo/", headers=headers)
                    if r.status_code == 200:
                        request.user = r.json()
                        # setattr(request, 'username', username)
                    else:
                        content = {"detail": "Authentication credentials were not provided."}
                        return HttpResponseAuthenticationFailed(json.dumps(content))
            except:
                pass
                # content = {"detail": "Authentication credentials were not provided."}
                # return HttpResponseAuthenticationFailed(json.dumps(content))


