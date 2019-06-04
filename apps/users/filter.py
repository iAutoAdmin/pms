import django_filters
from django.contrib.auth import get_user_model

User = get_user_model()
from permission.models import Permission


class UserFilter(django_filters.FilterSet):
    """
    用户搜索类
    """
    username = django_filters.CharFilter(lookup_expr='icontains', help_text='请输入用户名')

    class Meta:
        model = User
        fields = ['username', ]


class PermissionFilter(django_filters.FilterSet):
    codename = django_filters.CharFilter(name="codename", lookup_expr='icontains', help_text='请输入codename')

    class Meta:
        model = Permission
        fields = ['codename', ]
