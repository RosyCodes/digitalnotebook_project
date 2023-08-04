from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator
from datetime import datetime
from django.utils import timezone

from .choices import pdf_choices
from .models import Note
from .models import Notebook


# libraries for pdf generator
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views.generic import ListView

class NotesListView(ListView):
     model = Note
     template_name = 'notes/notes2pdf.html'



def index(request):
    # sort notes according to most recent and only the published ones
    my_notes = Note.objects.order_by('-note_date').filter(is_published=True)

    # show 3 notes across several pages
    paginator = Paginator(my_notes,6)
    page = request.GET.get('page')
    paged_notes = paginator.get_page(page)
    context = {
        'my_notes':paged_notes
    }
    return render(request,'notes/notes.html',context)

def note(request,note_id):
    # get the details of individual note using primary key
    note = get_object_or_404(Note,pk=note_id)

    context = {
        'note': note
    }
    return render(request,'notes/note.html',context)

def note_render_pdf_views(request,*args,**kwargs):
    note_id = kwargs.get('note_id')
    note = get_object_or_404(Note,pk=note_id)
    current_datetime = timezone.now()
    template_path = 'notes/notes2pdf.html'

    context = {
        'note': note,
        'current_datetime': current_datetime,
        }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    
    # if download note as pdf:
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    
    # if display notes as pdf
    response['Content-Disposition'] =  'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def search(request):
    # get the notes based on the search criteria while connecting to other table

    queryset_list = Note.objects.order_by('-note_date').filter(is_published=True)
    
    # keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(main_content__icontains=keywords) 

    # topic
    if 'topic' in request.GET:
        topic = request.GET['topic']
        if topic:
            queryset_list = queryset_list.filter(topic__icontains=topic) 

    # with pdf attachments
    if 'with_pdf' in request.GET:
        with_pdf = request.GET['with_pdf']
        if with_pdf=='yes':
            queryset_list = queryset_list.exclude(upload__exact='')
        if with_pdf=='no':
            queryset_list = queryset_list.exclude(upload__icontains='uploads')


    # speaker
    if 'speaker' in request.GET:
        speaker = request.GET['speaker']
        if speaker:
            queryset_list = queryset_list.filter(speaker__icontains=speaker) 
       

    context = {
    'pdf_choices':pdf_choices,
     'my_notes' : queryset_list,
     'values' : request.GET
    }
    return render(request,'notes/search.html',context)