from celery import Celery

# Инициализация Celery
app = Celery('zakupki_tasks', broker='redis://localhost:6379/0')

# Настройка для тестирования в eager-режиме, если необходимо
# app.conf.task_always_eager = True
