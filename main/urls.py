from django.urls import path
from . import views


app_name='main'

urlpatterns = [

    path('recuirtments', views.TemplateView.as_view(template_name = "main/recruitment.html",extra_context={'title': 'Recruitment Company in Nigeria'}), name='recruitments'),
    path('employers', views.employer_page, name='employers'),
    path('find-candidates', views.FindCandidatesView.as_view(), name='find-candidates'),
    path('contact', views.contact, name='contact'),
    path('help', views.help_view, name='help-view'),
    path('subscribe-to-a-newsletter', views.subscribe_to_a_newsletter, name='subscribe-to-a-newsletter'),
    
    
     
]



