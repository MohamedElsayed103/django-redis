from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Default Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'redisProject.settings')

app = Celery('redisProject')

# Redis as broker and result backend
app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.result_backend = 'redis://localhost:6379/0'

# Optional JSON configuration
app.conf.accept_content = ['json']
app.conf.task_serializer = 'json'
app.conf.result_serializer = 'json'
app.conf.timezone = 'Africa/Cairo'

# Auto-discover tasks from all apps
app.autodiscover_tasks()
