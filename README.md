# 云课堂学习平台

## window系统如何本地运行项目

1.首先运行web前端项目Node 20.6.1版本，运行命令npm run serve

2.运行本机redis数据库

3.如果没有虚拟环境，则运行python venv venv创建虚拟环境

4.有虚拟环境就在server项目根目录下激活虚拟环境venv\Scripts\activate

5.再运行pip install -r requirements.txt安装依赖包

6.运行后端服务器的celery工具，在server根目录下运行celery -A config worker --pool=solo --loglevel=info

7.运行后端服务器的celery-beat工具，在server根目录下运行celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

8.运行后端服务器的flower工具，在server根目录下运行celery -A config flower --basic-auth=andy:andygogo

9.运行后端服务器的django项目，在server根目录下运行python manage.py runserver 

## 其他资料

1.网盘资源 链接: https://pan.baidu.com/s/1j4c3cNe_5T_mgGD9fw1_Bg?pwd=8855 提取码: 8855

将python项目虚拟环境使用的包导出到文件命令：pip freeze > requirements.txt
