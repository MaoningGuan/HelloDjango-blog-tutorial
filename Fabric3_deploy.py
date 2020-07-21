# -*- coding: utf-8 -*-
"""
使用 Fabric 编写自动部署脚本
"""
# 1.  创建一个远程连接
# 2. 进入指定目录
# 3. 在指定目录下面执行重启命令
from fabric import Connection
from invoke import Responder
from _credentials import github_username, github_password


def _get_github_auth_responders():
    """
    返回 GitHub 用户名密码自动填充器
    """
    username_responder = Responder(
        pattern="Username for 'https://github.com':",
        response='{}\n'.format(github_username)
    )
    password_responder = Responder(
        pattern="Password for 'https://{}@github.com':".format(github_username),
        response='{}\n'.format(github_password)
    )
    return [username_responder, password_responder]


def deploy():
    supervisor_conf_path = '~/etc/'
    supervisor_program_name = 'hellodjango-blog-tutorial'

    project_root_path = '~/apps/HelloDjango-blog-tutorial/'

    # 如果你的电脑配了ssh免密码登录，就不需要 connect_kwargs 来指定密码了。
    c = Connection("root@106.53.196.251", connect_kwargs={"password": "Mm187020"})

    # 先停止应用
    with c.cd(supervisor_conf_path):
        cmd = 'supervisorctl -c ~/etc/supervisord.conf stop {}'.format(supervisor_program_name)
        c.run(cmd)

    # 进入项目根目录，从 Git 拉取最新代码
    with c.cd(project_root_path):
        cmd = 'git pull'
        responders = _get_github_auth_responders()
        c.run(cmd, watchers=responders)

    # 安装依赖，迁移数据库，收集静态文件
    with c.cd(project_root_path):
        c.run('pipenv install --deploy --ignore-pipfile')
        c.run('pipenv run python manage.py migrate')
        c.run('pipenv run python manage.py collectstatic --noinput')

    # 重新启动应用
    with c.cd(supervisor_conf_path):
        cmd = 'supervisorctl -c ~/etc/supervisord.conf start {}'.format(supervisor_program_name)
        c.run(cmd)


if __name__ == '__main__':
    deploy()