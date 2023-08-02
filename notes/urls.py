from django.urls import path
from . import views
from .views import NotesListView

urlpatterns = [
    path('',views.index,name='notes'),
    path('',NotesListView.as_view(),name='note-list-view'),
    path('pdf/<int:note_id>',views.note_render_pdf_views,name='note-pdf-view'),
    path('<int:note_id>',views.note,name='note'),
    path('search',views.search,name='search'),
]
