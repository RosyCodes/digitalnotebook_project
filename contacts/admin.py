from django.contrib import admin

from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    # model for user who leaves a message
    list_display = ('id','name','note','email','contact_date')
    list_display_links = ('id','name')
    search_fields = ('name','email','note')
    list_per_page = 25


admin.site.register(Contact,ContactAdmin)
