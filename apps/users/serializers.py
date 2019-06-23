from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()
from permission.models import Permission


class UserSerializer(serializers.ModelSerializer):
    """
    用户序列化类
    """
    username    = serializers.CharField(required=False, read_only=False, max_length=32, label="用户名", help_text="用户名")
    name        = serializers.CharField(required=False, read_only=False, label="姓名", help_text="姓名")
    is_active   = serializers.BooleanField(required=False, label="登陆状态", help_text="登陆状态")
    email       = serializers.CharField(read_only=True, help_text="联系邮箱")
    last_login  = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", help_text="上次登录时间")
    phone       = serializers.CharField(required=False, max_length=11, min_length=11, allow_null=True, help_text="手机号",
                                        error_messages={"max_length": "手机号错误", "min_length": "手机号错误"},
                                        )

    class Meta:
        model = User
        fields = ("id", "username", "name", "phone", "email", "is_active", "last_login")

class UserInfoSerializer(serializers.Serializer):
    """
    用户序列化类
    """
    id = serializers.IntegerField()
    username = serializers.CharField(required=False, max_length=32, label="用户名", help_text="用户名")
    email = serializers.CharField(help_text="联系邮箱")

    def get_user_permission(self, userobj):
        res = []
        ret = {}
        if userobj is not None:
            for group in userobj.groups.all():
                for p in group.pms_group.all():
                    res.append(p.codename)
            # print(res)
        for perobj in Permission.objects.all():
            if perobj.codename in res:
                ret[perobj.codename] = True
            else:
                ret[perobj.codename] = False
        return ret

    def to_representation(self, instance):
        permissions = self.get_user_permission(instance)
        ret = super(UserInfoSerializer, self).to_representation(instance)
        ret["permissions"] = permissions
        return ret
