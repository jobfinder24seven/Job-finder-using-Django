from django.forms import ModelForm
from accounts.models import *
from django.utils.translation import gettext_lazy as _


class NotificationEmployerForm(ModelForm):
    
    class Meta:
        model= Employer
        fields= ['subscribed_to_newsletter',]

        labels = {
            'subscribed_to_newsletter': _('Newsletter'),
        
            }

        
class NotificationJobSeekerForm(ModelForm):
    
    class Meta:
        model= JobSeeker
        fields= ['subscribed_to_newsletter',]
       