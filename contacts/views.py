from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact

def contact(request):
    if request.method == 'POST':
        note_id = request.POST['note_id']
        topic = request.POST['topic']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        
        # check if user has made a comment already
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(note_id=note_id,user_id=user_id)
            if has_contacted:
                messages.error(request,'You have left a message already.')
                return redirect('/notes/'+note_id)


        contact = Contact(note_id=note_id,note=topic,name=name,email=email,phone=phone,message=message,user_id=user_id)
        
        contact.save()

        messages.success(request,'Your message has been submitted. The author will reach out to you soon.')
        return redirect('/notes/'+note_id)
