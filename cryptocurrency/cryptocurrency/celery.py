from celery import Celery
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cryptocurrency.settings")

app = Celery("cryptocurrency")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'request: {self.request!r}')