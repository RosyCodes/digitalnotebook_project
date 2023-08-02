from django.db import models
from datetime import datetime
from django.conf import settings


# table model that is created unto the database
class Notebook(models.Model):
    title = models.CharField(max_length=200)
    course = models.CharField(max_length=100,blank=True)
    description = models.TextField(blank=True)
    photo_cover = models.ImageField(upload_to='photos/%Y/%m/%d/')
    is_published = models.BooleanField(default=True)
    notebook_date = models.DateTimeField(default=datetime.now,blank=True)
    is_mvp = models.BooleanField(default=False)
    user =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
   
    # returns the title of the notebook whenever this class  is called
    def __str__(self):
        return self.title
        
    


