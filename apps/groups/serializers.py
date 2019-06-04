from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers

User = get_user_model()


class GroupSerializer(serializers.ModelSerializer):
    """
    用户组序列化类
    """

    def get_node(self, node_queryset):
        ret = []
        for node in node_queryset:
            ret.append(node.node_name)
        return ret

    def get_permissions(self, permission_queryset):
        ret = []
        for per in permission_queryset:
            ret.append(per.codename)
        return ret

    def get_users(self, users_queryset):
        ret = []
        for u in users_queryset:
            ret.append(u.username)
        return ret

    def to_representation(self, instance):
        nodes = self.get_node(instance.node_group.all())
        permissions = self.get_permissions(instance.pms_group.all())
        member = self.get_users(instance.user_set.all())
        # member = instance.user_set.all()
        ret = super(GroupSerializer, self).to_representation(instance)
        ret["nodes"] = nodes
        ret["permissions"] = permissions
        ret["member"] = member
        return ret

    class Meta:
        model = Group
        fields = ("id", "name")
