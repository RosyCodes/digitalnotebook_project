from django.db import models
from datetime import datetime
from django.utils import timezone

class Contact(models.Model):
    note = models.CharField(max_length=200)
    note_id = models.IntegerField()
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    message  = models.TextField(blank=True)
    contact_date = models.DateTimeField(default=timezone.now,blank=True)
    user_id =  models.IntegerField(blank=True)

    def __str__(self):
        return self.name