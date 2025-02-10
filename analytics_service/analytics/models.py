from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=255, unique=True)
    base_url = models.URLField()

    def __str__(self):
        return self.name

class RequestData(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    response_time = models.FloatField(null=True)
    success = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['service']),
        ]