import django_filters
from permission.models import PerAppName, NodeInfo, Permission


class PerAppNameFilter(django_filters.FilterSet):
    '''
    AppName 搜索类
    '''
    app_name = django_filters.CharFilter(lookup_expr='icontains', help_text='过滤app名称')

    class Meta:
        model = PerAppName
        fields = ['app_name']


class NodeinfoFilter(django_filters.FilterSet):
    '''
    NodeName 搜索类
    '''
    node_name = django_filters.CharFilter(lookup_expr='icontains', help_text='过滤node节点名称')

    class Meta:
        model = NodeInfo
        fields = ['node_name']


class PermissionFilter(django_filters.FilterSet):
    '''
    Permission 搜索类
    '''
    codename = django_filters.CharFilter(lookup_expr='icontains', help_text='过滤权限名称')

    class Meta:
        model = Permission
        fields = ['codename']
