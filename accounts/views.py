from django.utils.encoding import force_str
from django.contrib.auth import get_user_model

from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator


from contacts.models import Contact
from notebooks.models import Notebook
from notes.models import Note
from sharednotes.models import SharedNote
from .forms import NotebookForm
from .forms import NoteForm

def register(request):
    # Register User
    if request.method == 'POST':
        # Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # check if passwords match
        if password == password2:
            # check form's username with the table's username
            if User.objects.filter(username=username).exists():
                messages.error(request,'That username is taken. ')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request,'That email is being used. ')
                    return redirect('register')
                else:  
                    # user credentials are valid and unique, save
                    user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
                    
                     # Send confirmation email
                    if user:
                        # Generate the token for the confirmation link
                        token = default_token_generator.make_token(user)
                        uid = urlsafe_base64_encode(force_bytes(user.pk))
                        domain = get_current_site(request).domain
                        confirm_url = reverse('confirm_registration', kwargs={'uidb64': uid, 'token': token})
                        confirmation_link = f"http://{domain}{confirm_url}"

                        subject = 'Confirmation Email'
                        html_message = render_to_string('accounts/confirmation_email.html', {
                            'user': user,
                            'domain': domain,
                            'confirmation_link': confirmation_link,
                        })

                    
                        # Create plain text version by stripping HTML tags
                        text_message = strip_tags(html_message)

                        # Send the email using EmailMultiAlternatives
                        msg = EmailMultiAlternatives(subject, text_message, 'rnldevsolutions@gmail.com', [user.email])
                        msg.attach_alternative(html_message, "text/html")
                        msg.send()

                        messages.success(request, 'You are now registered. A confirmation email has been sent to your email address. Please click the link in the email to confirm your registration.')
                        return redirect('login')


        else:
            messages.error(request,'Passwords do not match')
            return redirect('register')
    else:
        return render(request,'accounts/register.html')


def confirm_registration(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated. You can now log in.')
    else:
        messages.error(request, 'The confirmation link is invalid or has expired. Please try again or contact support.')

    return redirect('login')

def login(request):
     # Login User
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request,'Invalid credentials.')
            return redirect('login')
    else:
        return render(request,'accounts/login.html')

def logout(request):
     # Login User
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request,'You are now logged out.')    
        return redirect('index')

def dashboard(request):
  
     # get all the messages for the logged in user
    user_contacts =  Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
    context = {
       
        'contacts': user_contacts
    }
    return render(request,'accounts/dashboard.html',context)

def viewnotebook(request):
    # get all the notebooks for the logged in user
    user_notebooks =  Notebook.objects.order_by('-notebook_date').filter(user_id=request.user.id)
    
      # show 6 notebooks across several pages
    paginator = Paginator(user_notebooks,6)
    page = request.GET.get('page')
    paged_notebooks = paginator.get_page(page)

    context = {
        'usernotebooks': paged_notebooks
    }
    return render(request,'accounts/viewnotebook.html',context)



def viewnotes(request,notebook_id):
    # get all the notes for the logged in user
    user_notes =  Note.objects.all().filter(notebook_id=notebook_id)
  
    context = {
        'user_notes': user_notes
    }
    return render(request,'accounts/viewnotes.html',context)

def createnotebook(request):
     # create new notebook for authorized user
    if request.method == 'POST':
        form = NotebookForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']

            # Check if a notebook with the same title already exists
            if Notebook.objects.filter(title=title, user_id=request.user.id).exists():
                messages.error(request, 'A notebook with this title already exists. Please choose a different title.')
                return redirect('createnotebook')
            
            notebook = form.save(commit=False)
            notebook.user_id = request.user.id
            notebook.save()
            messages.success(request, 'You have successfully created a new notebook.')
            return redirect('viewnotebook')
        else:
            print(form.errors)
            messages.error(request, 'Please complete required fields.')
            return redirect('createnotebook')
    else:
        form = NotebookForm(initial={'user_id': request.user.id})
    
    context = {
        'form': form
    }
    return render(request, 'accounts/createnotebook.html', context)





def addnote(request,notebook_id):
   # Get the notebook object or return a 404 page if not found
    notebook = get_object_or_404(Notebook, id=notebook_id)

    # Check if the current user owns the notebook
    if request.user.id != notebook.user_id:
        return redirect('viewnotebook')  

    if request.method == 'POST':

        form = NoteForm(request.POST,request.FILES)
               
        if form.is_valid():
            note = form.save(commit=False)
            note.notebook = notebook
        
            note.save()
            messages.success(request, 'You have succesfully created a new note.')
            return redirect('viewnotebook')
        else:
            
            messages.error(request,'Please complete required fields. ')
            return redirect('addnote',notebook_id)
            
                
    else:
        
        form = NoteForm(initial={'notebook': notebook_id})
    
    context = {
   
        'notebookid': notebook.id,
        'notebooktitle':notebook.title,
        'form': form
            }
    return render(request,'accounts/addnote.html',context)
    

def deletenotebook(request, notebook_id):
    # delete a notebook for authorized user
    notebook = Notebook.objects.get(id=notebook_id)

    if request.method == 'POST':
        notebook.delete()
        messages.success(request, 'You have succesfully deleted a notebook.')
        return redirect('viewnotebook')  

    return render(request, 'accounts/deletenotebook.html', {'notebook': notebook})


def updatenotebook(request, notebook_id):
     # update a notebook for authorized user
    notebook = get_object_or_404(Notebook, id=notebook_id, user=request.user)

    if request.method == 'POST':
        form = NotebookForm(request.POST, request.FILES, instance=notebook)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notebook updated successfully.')
            return redirect('viewnotebook')
    else:
        form = NotebookForm(instance=notebook, initial={'user_id': notebook.user_id})

    context = {
        'form': form,
        'notebook': notebook,
        'userid': request.user.id
    }
    return render(request, 'accounts/updatenotebook.html', context)

def editnote(request, notebook_id, note_id):
     # update a note of a given notebook for authorized user
    note = get_object_or_404(Note, id=note_id)

    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, 'Note updated successfully.')
            
            return redirect(reverse('note', args=[note_id]))
        else:
            messages.error(request, 'Please complete required fields.')

    else:
        form = NoteForm(instance=note)

    context = {
        'form': form,
        'note': note,

    }
    return render(request, 'notes/editnote.html', context)

def deletenote(request, note_id):
     # delete a note for authorized user
    note = Note.objects.get(id=note_id)

    if request.method == 'POST':
        note.delete()
        messages.success(request, 'You have succesfully deleted a note.')
        return redirect('viewnotebook')  

    return render(request, 'notes/deletenote.html', {'note': note})


def viewmessage(request, note_id):
    # Get the Note object associated with the given note_id
    note = get_object_or_404(Note, id=note_id)
    # Get the message associated with the user for the given note_id
    messages = Contact.objects.all().filter(note_id=note_id)

    context = {
        'note':note,
        'messages': messages,
    }
    return render(request, 'accounts/viewmessage.html', context)

def sharenote(request, note_id):
     # get the note details for a specific note of a  authorized user
    note = Note.objects.get(id=note_id)
    shared_note = SharedNote.objects.create(note=note, user=request.user)  # Pass the logged-in user
    shared_link_url = request.build_absolute_uri(shared_note.get_absolute_url())

    return render(request, 'notes/sharednote.html', {'note': note, 'shared_link_url': shared_link_url})

def sharednotedetail(request, token):
     # provide a shareable link for a given note and store this link to database
    shared_note = get_object_or_404(SharedNote, token=token)
    note = shared_note.note
    shared_link_url = request.build_absolute_uri(shared_note.get_absolute_url())

    context = {
        'note': note,
        'shared_note': shared_note,
        'shared_link_url': shared_link_url,
    }
    return render(request, 'notes/sharednote.html', context)