from django.contrib import admin

from .models import Notebook

# Controls the fields that will be displayed on the admin site
class NotebookAdmin(admin.ModelAdmin):
    list_display=('id','title','course','is_published','notebook_date','is_mvp')
    list_display_links=('id','title')
    list_filter=('course',)
    list_editable=('is_published','is_mvp')
    search_fields = ('title','description','course')
    list_per_page = 25
    
admin.site.register(Notebook, NotebookAdmin)
