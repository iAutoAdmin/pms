from rest_framework.routers import DefaultRouter
from .views import GroupViewset, UserGroupsViewset


group_router = DefaultRouter()
group_router.register(r'groups', GroupViewset, base_name="groups")
group_router.register(r'usergroups', UserGroupsViewset, base_name="usergroups")