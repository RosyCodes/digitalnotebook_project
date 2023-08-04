from django.db import models
from datetime import datetime
from django.utils import timezone
from ckeditor.fields import RichTextField

from notebooks.models import Notebook

class Note(models.Model):
    notebook = models.ForeignKey(Notebook,on_delete=models.CASCADE) #FK to Notebook table
    topic = models.CharField(max_length=200)
    speaker = models.CharField(max_length=100,blank=True)
    main_content = RichTextField(blank=True,null=True)
    #main_content = models.TextField(blank=True)
    upload = models.FileField(upload_to='uploads/%Y/%m/%d/',blank=True)
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/')
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/',blank=True)
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/',blank=True)
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/',blank=True)
    photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d/',blank=True)
    photo_5 = models.ImageField(upload_to='photos/%Y/%m/%d/',blank=True)
    photo_6 = models.ImageField(upload_to='photos/%Y/%m/%d/',blank=True)
    is_published = models.BooleanField(default=True)
    note_date = models.DateTimeField(default=timezone.now,blank=True)
    
    
    def __str__(self):
        return self.topic