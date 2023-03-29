from django import forms
from django.forms import ModelForm
from main.models import *
from django.utils.translation import gettext_lazy as _


class NewsletterForm(ModelForm):
    
    class Meta:
        model= Newsletter
        fields= "__all__"
        labels = {
            'subject': _('Subject'),
            'body':_('Body'),
            'email':_('Email'),
            'status':_('Status'),
            }

class NewsletterForm(forms.Form):
	subject = forms.CharField(max_length = 250)
	message = forms.CharField(widget = forms.Textarea, max_length = 10_000)
 
class ContactForm(forms.Form):
	full_name = forms.CharField(max_length = 250)
	subject = forms.CharField(max_length = 50)
	email_address = forms.EmailField(max_length = 150)
	message = forms.CharField(widget = forms.Textarea, max_length = 2000)