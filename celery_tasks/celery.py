from celery import Celery

app = Celery('celery_tasks')
app.config_from_object('celery_tasks.celeryconfig')

# 自动搜索任务
app.autodiscover_tasks(['celery_tasks'])