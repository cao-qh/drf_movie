@echo off
start cmd /k  redis-server.exe
start cmd /k  "cd web && npm run serve"
start cmd /k  "cd server && venv\Scripts\activate && celery -A config worker --pool=solo --loglevel=info"
start cmd /k  "cd server && venv\Scripts\activate && celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler"
start cmd /k  "cd server && venv\Scripts\activate && celery -A config flower --basic-auth=andy:andygogo"
start cmd /k  "cd server && venv\Scripts\activate && python manage.py runserver"