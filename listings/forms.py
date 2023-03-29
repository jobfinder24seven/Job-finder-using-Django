from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm,Textarea
from .models import Job

class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = '__all__'
        exclude=['created_by']
        widgets = {
            'description': Textarea(attrs={'cols': 40, 'rows': 5}),
            'requirements': Textarea(attrs={'cols': 40, 'rows': 5}),
            'application_mode': Textarea(attrs={'cols': 40, 'rows': 5}),   
        }
        labels = {
            'company_name': _('Company Name'),
            'email': _('Email'),
            'website': _('Website'),
            'title': _('Job Title'),
            'location': _('Location'),
            'country': _('Country'),
            'salary': _('Min-Max salary'),
            'type': _('Job Type'),
            'experience': _('Experience'),
            'description ': _('Description '),
            'requirements': _('Requirements'),
            'logo': _('Company logo'),
            'closed_at': _('Deadline'),
        }
        help_texts = {
            # 'company_name': _('Company Name'),
            # 'email': _('Email'),
            # 'website': _('Website'),
            # 'title': _('Job Title'),
            # 'location': _('Location'),
            # 'country': _('Country'),
            # 'min_salary': _('Min.Salary'),
            # 'max_salary': _('Max.Salary'),
            # 'type': _('Job Type'),
            # 'experience': _('Experience'),
            # 'description ': _('Description '),
            # 'requirements': _('Requirements'),
        }
        error_messages = {
            'name': {
                'max_length': _("This writer's name is too long."),
            },
        }
    
  