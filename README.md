# pms

#### 项目介绍
权限管理系统简称PMS(Permission Manager System),pms系统主旨为内部应用APP，用户与权限，用户组和权限提供一个授权认证机制

#### 软件架构
- pms-web(为前端vue框架，使用模版为vueadmin-element)
- pms(django rest framework + mysql5.7)

#### 安装教程

1. pip install -r requirements.txt

#### 接口使用说明

1. http://127.0.0.1:8000/perappname/
  - 为各个子系统生成唯一凭证，并作为后续访问依据
2. http://127.0.0.1:8000/authper/
  - 子系统验证接口
3. http://127.0.0.1:8000/nodeinfo/
  - node节点增删改查
4. http://127.0.0.1:8000/nodeinfomanage/
  - 无限级分类展示node节点信息
5. http://127.0.0.1:8000/permission/
  - 子系统权限接口
6. http://127.0.0.1:8000/userinfo/
  - 返回用户个人信息
7. http://127.0.0.1:8000/userinfo/?username=mt
  - 查询用户权限信息
8. http://127.0.0.1:8000/userinfo/?username=mt&&codename=pms_a_node
  - 验证用户单个权限信息
9. http://127.0.0.1:8000/userinfo/?username=mt&&codename=pms_a_node&&codename=pms_d_node
  - 验证用户多个权限信息

#### 更多详细接口参数请访问http://127.0.0.1:8000/docs/

