#!/usr/bin/env python
# -*- coding: utf-8 -*-


from rest_framework.routers import DefaultRouter
from .views import PerAppNameViewSet, NodeInfoViewSet, NodeInfoManageViewSet, AuthPerViewSet, PermissionViewSet


pms_router = DefaultRouter()
pms_router.register("perappname", PerAppNameViewSet, base_name='perappname')
pms_router.register("authper", AuthPerViewSet, base_name='authper')
pms_router.register("nodeinfo", NodeInfoViewSet, base_name='nodeinfo')
pms_router.register("nodeinfomanage", NodeInfoManageViewSet, base_name='nodeinfomanage')
pms_router.register("permission", PermissionViewSet, base_name='permission')
