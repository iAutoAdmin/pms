from rest_framework.routers import DefaultRouter
from .views import GroupViewset, UserGroupsViewset, GroupMembersViewset, GroupPermissionViewset


group_router = DefaultRouter()
group_router.register(r'groups', GroupViewset, base_name="groups")
group_router.register(r'usergroups', UserGroupsViewset, base_name="usergroups")
group_router.register(r'groupmembers', GroupMembersViewset, base_name="groupmembers")
group_router.register(r'grouppermission', GroupPermissionViewset, base_name="grouppermission")