from django.db import models
from django.utils import timezone


class News(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)

    def __str__(self):
        return self.title
