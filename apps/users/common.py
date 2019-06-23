from django.contrib.auth import get_user_model

User = get_user_model()

def get_user_obj(uid):
    try:
        for id in uid:
            if User.objects.get(pk=id):
                pass
        return uid
    except User.DoesNotExist:
        return None