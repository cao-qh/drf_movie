# 云课堂学习平台

## window系统如何本地运行项目

1.首先运行web前端项目Node 20.6.1版本，运行命令npm run serve

2.运行本机redis数据库

3.运行后端服务器的celery工具，在server根目录下运行celery -A config worker --pool=solo --loglevel=info

4.运行后端服务器的celery-beat工具，在server根目录下运行celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

5.运行后端服务器的flower工具，在server根目录下运行celery -A config flower --basic-auth=andy:andygogo

