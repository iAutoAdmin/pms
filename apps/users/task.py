import copy
import os
import sys
import django
import requests

project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(project_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pms.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()


class sync_user(object):
    def __init__(self):
        self.__user = "test"
        self.__password = "abcd.1234"
        self.url = "http://101.200.61.189:52131"
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        self.__base_data = dict(
            username=self.__user,
            password=self.__password,
        )

        self.__token = self.get_token()

    def get_token(self):
        params = copy.deepcopy(self.__base_data)
        ret = requests.post(url=self.url + '/api-token-auth/', verify=False, headers=self.headers, json=params)
        ret_json = ret.json()
        token = ret_json['token']
        return token

    @property
    def get_user(self):
        data = []
        headers = {"Authorization": "JWT " + self.get_token()}
        for i in range(1, 10):
            r = requests.get("http://101.200.61.189:52131/users/?page={}".format(i), headers=headers)
            if r.json(['results']):
                data.extend(r.json()['results'])
        return data

    def create_user(self):
        data = self.get_user
        print(data)
        user_obj = User()
        ret = {}
        try:
            for user in data:
                user_obj.id = user['id']
                user_obj.username = user['username']
                user_obj.name = user['name']
                user_obj.phone = user['phone']
                user_obj.email = user['email']
                user_obj.is_active = user['is_active']
                user_obj.last_login = user['last_login']
                user_obj.save()
            ret['status'] = 1
            return ret
        except:
            ret['status'] = 0
            return ret


if __name__ == '__main__':
    info = sync_user()
    print(info.get_token())
    print(info.get_user)
    info.create_user()
