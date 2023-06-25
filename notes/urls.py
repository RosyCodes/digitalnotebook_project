from django.urls import path
from . import views
from .views import render_pdf_view, NotesListView,note_render_pdf_views

urlpatterns = [
    path('',views.index,name='notes'),
    path('',NotesListView.as_view(),name='note-list-view'),
    path('pdf/<int:note_id>',note_render_pdf_views,name='note-pdf-view'),
    path('<int:note_id>',views.note,name='note'),
    path('search',views.search,name='search'),
]
