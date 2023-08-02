
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime
from notes.models import Note
import uuid

class SharedNote(models.Model):
    note = models.ForeignKey('notes.Note', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=150, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


    def get_absolute_url(self):
        return reverse('sharednotedetail', kwargs={'token': self.token})