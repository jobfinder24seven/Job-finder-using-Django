from django.shortcuts import render,redirect
from . models import *
from django.contrib import messages
from django.http import Http404
from django.views.generic.base import TemplateView
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.conf import settings


    
class FindCandidatesView(TemplateView):

    template_name = "main/find_candidates.html" 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Candidate search - Fast search candidate's resume" 
        return context
    

def subscribe_to_a_newsletter(request):
    if request.method =="POST":
        subscriber_email = request.POST.get('email').lower()
        
        if subscriber_email.lower():
            
            # check if users exists
            if NewsletterSubscriber.objects.filter(email=subscriber_email).exists():
                messages.error(request, "You're already a subscriber")
                return redirect('/')
            else:
                newsletter_subscriber = NewsletterSubscriber()
                newsletter_subscriber.email =subscriber_email
                newsletter_subscriber.save()
                messages.success(request, "Congrats, your email has been reactivated to receive job alert")
                return render(request, 'accounts/signup.html',{'sub':subscriber_email}) 
        else:
            return render(request, 'accounts/signup.html')
    else:
        #return redirect('404')
        raise Http404("Bad format")
    
def employer_page(request):
	form = ContactForm()
	return render(request, "main/employers.html", {"title":'Recruitment Company in Nigeria','form':form})
        

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            full_name = form.cleaned_data['full_name']
            email=form.cleaned_data['email_address']
            message=form.cleaned_data['message']
            try:
                
                send_mail(subject, message, email, [settings.EMAIL_HOST_USER])
                messages.success(request, "email sent")
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect ("main:employers")
        

def help_view(request):
	form = ContactForm()
	return render(request, "main/help.html", {"title":'Help','form':form})
        