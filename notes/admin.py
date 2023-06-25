from django.contrib import admin

from .models import Note

# Controls the fields that will be displayed on the admin site
class NoteAdmin(admin.ModelAdmin):
    list_display=('id','topic','speaker','is_published','note_date','notebook')
    list_display_links=('id','topic')
    list_filter=('notebook',)
    list_editable=('is_published',)
    search_fields = ('topic',)
    list_per_page = 25

admin.site.register(Note,NoteAdmin)
