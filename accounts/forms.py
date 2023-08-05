from django import forms
from django.forms import ModelForm

from notebooks.models import Notebook
from notes.models import Note

from datetime import datetime

# create a Notebook form
class NotebookForm(ModelForm):
   

    class Meta:
        
        model = Notebook
        exclude = ['user_id']
        # use this instead if you want all fields
        #fields = "__all__"
        
        # Define the labels for the form fields
        labels = {
            'is_mvp': 'Mark as Valuable Notebook:',
            'is_published': 'Publish Publicly:',
            'notebook_date': 'Date Created',
            'photo_cover': 'Upload notebook main image',          
        }


        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'course': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control','cols':80,'rows':5}),
            'notebook_date': forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Exclude the 'user' field from the form
        self.fields.pop('user')


# create a Note form
class NoteForm(ModelForm):
   
    class Meta:     
        model = Note
        exclude = ['notebook_id']
        

        labels = {
            'upload': 'Attach files to upload:',
            'is_published': 'Publish Publicly:',
            'note_date': 'Date Created',
            'photo_main': 'Upload primary image',          
        }
       
        widgets = {
            
            'topic': forms.TextInput(attrs={'class':'form-control'}),
            'speaker': forms.TextInput(attrs={'class':'form-control'}),
            'main_content': forms.Textarea(attrs={'class':'form-control','cols':80,'rows':10}),
            'note_date': forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S'),
            
        }
    

