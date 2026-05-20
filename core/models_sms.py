from django.db import models

class SmsSubscriber(models.Model):
    phone = models.CharField(max_length=20, unique=True)
    subscribed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone
