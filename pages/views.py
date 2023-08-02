from django.shortcuts import render
from django.http import HttpResponse

from notes.choices import pdf_choices
from notes.models import Note
from notebooks.models import Notebook

# Home Page
def index(request):
    # show only 3 most recent notes on the home page 
    my_notes = Note.objects.order_by('-note_date').filter(is_published=True)[:3]
    context = {
        'my_notes':my_notes,
        'pdf_choices':pdf_choices
    }
    
    return render(request,'pages/index.html',context)

# About Page
def about(request):
    # get all the notebooks created
    my_notebooks = Notebook.objects.order_by('-notebook_date')[:3]
    
    # get the 1 most valuable notebook 
    mvp_notebooks = Notebook.objects.all().filter(is_mvp=True)[:3]
    
    context = {
        'my_notebooks': my_notebooks,
        'mvp_notebooks': mvp_notebooks
    }

    return render(request,'pages/about.html',context)