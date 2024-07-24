from django.db import models
from django.utils import timezone

class User(models.Model):
    fname = models.CharField(max_length=25)
    username = models.CharField(max_length=25)
    chat_id = models.CharField(max_length=50, unique=True)
    sub_status = models.CharField(max_length=25, default="trial")

    def __str__(self):
        return f"{self.fname} ({self.username})"

class Link(models.Model):
    original = models.URLField()
    short_code = models.CharField(max_length=10, unique=True)
    date_created = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, related_name='links', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.original} ({self.short_code})"
