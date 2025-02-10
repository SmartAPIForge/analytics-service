from celery import shared_task
import requests
from django.utils import timezone
from .models import Service, RequestData
import time

@shared_task
def make_requests():
    services = Service.objects.all()
    for service in services:
        for _ in range(10):
            start_time = time.time()
            try:
                response = requests.get(service.base_url, timeout=10)
                response.raise_for_status()
                RequestData.objects.create(
                    service=service,
                    timestamp=timezone.now(),
                    response_time=time.time() - start_time,
                    success=True
                )
            except Exception as e:
                RequestData.objects.create(
                    service=service,
                    timestamp=timezone.now(),
                    response_time=None,
                    success=False
                )