from django.db import models
from django.contrib.auth.models import Group


class PerAppName(models.Model):
    app_key = models.CharField("APPkey", max_length=64, null=False, unique=True, help_text="APPkey")
    app_name = models.CharField("APP名称", max_length=32, null=False, blank=False, help_text="APP名称")
    app_desc = models.CharField("APP应用描述", max_length=32, blank=False, help_text="APP应用描述")

    def __str__(self):
        return self.app_name

    class Meta:
        db_table = "pms_app"


class NodeInfo(models.Model):
    node_name = models.CharField("节点名称", max_length=32, db_index=True, help_text="service名称")
    pid = models.IntegerField("节点pid", db_index=True, help_text="pid")
    path_node = models.CharField("节点中文path", max_length=32, db_index=True, help_text="node中文path")
    groups = models.ManyToManyField(Group, verbose_name="用户组关联节点", related_name="node_group", help_text="用户组关联节点")

    def __str__(self):
        return self.node_name

    class Meta:
        db_table = "pms_node"
        ordering = ["id"]


class Permission(models.Model):
    codename = models.CharField("权限简称", max_length=32, help_text="权限简称")
    desc = models.CharField("权限描述信息", max_length=32, help_text="权限描述信息")
    app = models.CharField("APP名称", max_length=32, help_text="APP名称")
    groups = models.ManyToManyField(Group, verbose_name="用户组关联权限", related_name="pms_group", help_text="用户组关联权限")

    def __str__(self):
        return self.codename

    class Meta:
        db_table = 'pms_permission'
        ordering = ['id']
