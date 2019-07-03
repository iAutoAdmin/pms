from rest_framework import viewsets, permissions, mixins, status
from rest_framework.response import Response
from django.contrib.auth.models import Group
from .serializers import GroupSerializer
from users.serializers import UserSerializer
from permission.serializers import PermissionSerializer
from users.common import get_user_obj, get_permission_obj
from .filter import GroupFilter
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()


class GroupViewset(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_class = GroupFilter
    filter_fields = ['name']

    def get_queryset(self):
        queryset = super(GroupViewset, self).get_queryset()
        queryset = queryset.order_by('id')
        return queryset


class GroupMembersViewset(mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    """
    角色成员管理
    retrieve:
    返回指定组的成员列表
    update:
    往指定组里添加成员
    destroy:
    从指定组里删除成员
    """
    queryset = Group.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        queryset = instance.user_set.all()
        username = request.GET.get("username", None)
        if username is not None:
            queryset = queryset.filter(Q(name__icontains=username) | Q(username__icontains=username))
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        ret = {"status": 0}
        group_obj = self.get_object()
        userobj = get_user_obj(request.data.get("uid", 0))
        if userobj is None:
            ret["status"] = 1
            ret["errmsg"] = "用户错误"
        else:
            for id in userobj:
                group_obj.user_set.add(id)
        return Response(ret, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        ret = {"status": 0}
        group_obj = self.get_object()
        userobj = get_user_obj(request.data.getlist("uid", 0))
        if userobj is None:
            ret["status"] = 1
            ret["errmsg"] = "用户错误"
        else:
            for id in userobj:
                group_obj.user_set.remove(id)
        return Response(ret, status=status.HTTP_200_OK)


class GroupPermissionViewset(mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.DestroyModelMixin,
                             viewsets.GenericViewSet):
    """
    权限组管理
    retrieve:
    返回指定组的权限列表
    update:
    往指定组里添加权限
    destroy:
    从指定组里删除权限
    """
    queryset = Group.objects.all()
    serializer_class = PermissionSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        queryset = instance.pms_group.all()
        codename = request.GET.get("codename", None)
        if codename is not None:
            queryset = queryset.filter(codename__icontains=codename)
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        ret = {"status": 0}
        group_obj = self.get_object()
        per_obj = get_permission_obj(request.data.getlist("pid", 0))
        if per_obj is None:
            ret["status"] = 1
            ret["errmsg"] = "权限错误"
        else:
            for id in per_obj:
                group_obj.pms_group.add(id)
        return Response(ret, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        ret = {"status": 0}
        group_obj = self.get_object()
        per_obj = get_permission_obj(request.data.getlist("pid", 0))
        if per_obj is None:
            ret["status"] = 1
            ret["errmsg"] = "权限错误"
        else:
            for id in per_obj:
                group_obj.pms_group.remove(id)
        return Response(ret, status=status.HTTP_200_OK)
