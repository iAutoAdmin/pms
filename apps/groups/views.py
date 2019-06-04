from rest_framework import viewsets, permissions, mixins, status
from rest_framework.response import Response
from django.contrib.auth.models import Group
from .serializers import GroupSerializer
from users.serializers import UserSerializer
from users.common import get_user_obj
from rest_framework.pagination import PageNumberPagination
from .filter import GroupFilter
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()


class GroupViewset(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = PageNumberPagination
    # permission_classes = (permissions.IsAuthenticated,)
    filter_class = GroupFilter
    filter_fields = ['name']

    def get_queryset(self):
        queryset = super(GroupViewset, self).get_queryset()
        queryset = queryset.order_by('id')
        return queryset


class UserGroupsViewset(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):
    """
    retrieve:
    返回指定用户的所有角色
    update:
    修改当前用户的角色
    """
    queryset = User.objects.all()
    # serializer_class = GroupSerializer

    def retrieve(self, request, *args, **kwargs):
        user_obj = self.get_object()
        queryset = user_obj.groups.all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        user_obj = self.get_object()
        gids = request.data.get("gid", [])
        user_obj.groups = Group.objects.filter(id__in=gids)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        queryset = super(UserGroupsViewset, self).get_queryset()
        return queryset.order_by("id")
