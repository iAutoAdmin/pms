from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets, permissions, response, status
from .serializers import UserSerializer, UserInfoSerializer
from .filter import UserFilter
from rest_framework.pagination import PageNumberPagination
from pms.paginations import Pagination
from permission.models import Permission
from .task import sync_user

User = get_user_model()


class UsersViewset(viewsets.ModelViewSet):
    """
    retrieve:
        获取指定用户信息
    list:
        获取用户列表
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = (permissions.IsAuthenticated,)
    filter_class = UserFilter
    filter_fields = ("username",)
    extra_perms_map = {
        "GET": ["users.show_user_list"]
    }

    def get_queryset(self):
        queryset = super(UsersViewset, self).get_queryset()
        queryset = queryset.order_by("id")
        queryset = queryset.exclude(is_superuser=True)
        return queryset

class UserInfoViewset(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserInfoSerializer

    # permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        res = []
        ret = {}
        userobj = False
        perobj = False
        username = request.query_params.get('username', None)
        codename = request.query_params.getlist('codename', None)
        # 获取pms_permission的codename权限信息
        if codename:
            try:
                for code in codename:
                    perobj = Permission.objects.get(codename=code)
                    # 获取auth_permission表中codename
                    if perobj:
                        res.append(perobj.codename)
            except Permission.DoesNotExist:
                ret = {"status": 0, "msg": "请输入正确的用户名和codename"}
                return response.Response(ret)
        else:
            perobj = False

        if username:
            try:
                userobj = User.objects.get(username=username)
            except User.DoesNotExist:
                ret = {"status": 0, "msg": "请输入正确的用户名"}
                return response.Response(ret)

        if perobj and userobj:
            for i in res:
                if i in self.get_user_permission(userobj):
                    # 获取用户权限#
                    ret[i] = True
                else:
                    ret[i] = False

            return response.Response({"status": 1, "permission": ret})
        elif userobj:
            res = self.get_user_permission(userobj)
            # 获取用户对象的权限信息
            for m in Permission.objects.all():
                # 取出权限表中的所有权限信息
                if str(m) in res:
                    ret[str(m)] = True
                else:
                    ret[str(m)] = False
            return response.Response({'status': 1, 'username': username, 'permission': ret})
        else:
            return response.Response(
                {"id": self.request.user.id, "username": self.request.user.username})

    def get_user_permission(self, userobj):
        res = []
        if userobj is not None:
            for group in userobj.groups.all():
                for p in group.pms_group.all():
                    # 获取当前组所属的权限信息
                    res.append(p.codename)
                    # 给组增加新权限
            return res


class TestViewSet(viewsets.GenericViewSet):
    def get(self, request, *args, **kwargs):
        return response.Response("test")

    def list(self, request, *args, **kwargs):
        return response.Response("test")


class SyncUsersViewset(viewsets.GenericViewSet):
    """
    list:
        同步用户数据信息
    """
    def list(self, request, *args, **kwargs):
        sync = sync_user()
        res = sync.create_user()
        if res['status']:
            return response.Response({"status": 1, "msg": "数据同步成功"})
        else:
            return response.Response({"status": 0, "msg": "数据同步失败"})