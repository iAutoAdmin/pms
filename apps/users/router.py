from rest_framework.routers import DefaultRouter
from .views import UsersViewset, UserInfoViewset, TestViewSet, SyncUsersViewset


user_router = DefaultRouter()
user_router.register(r'users', UsersViewset, base_name="users")
user_router.register(r'userinfo', UserInfoViewset, base_name="userinfo")
user_router.register(r'test', TestViewSet, base_name="test")
user_router.register(r'sync_user', SyncUsersViewset, base_name="sync_user")