from django.utils import timezone
from django.views.generic.base import TemplateView
from django.contrib import messages
from . models import Job,Applicant
from core import extras 
from accounts.models import *
from django.views.generic.list import ListView
from django.http import Http404
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect, get_object_or_404
from django.core.mail import EmailMessage
from django.conf import settings
from . decorators import *

currentYear = datetime.now().year


class FreeJobPostPageView(TemplateView):
    template_name = "listings/free_job_post.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Free Job Posting' 
        return context
    
class FeaturedJobPostingPageView(TemplateView):

    template_name = "listings/featured_job_posting.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Featured Job Posting' 
        return context
    
@employer_required
def create_job_View(request):
    """
    Provide the ability to create job post
    """
    context={}
    user = CustomUser.objects.get(id=request.user.id)
    employer_id = Employer.objects.get(user_id=user)

    context['title'] ='Create-Job'
    context['employer'] = employer_id
    context['locations'] = extras.LOCATION_CHOICES
    context['countries'] = extras.COUNTRY_CHOICES
    context['job_types'] = extras.JOB_TYPE_CHOICES
    context['experience'] = extras.EXP_CHOICES
    context['qualifications'] = extras.QUALIFICATION_CHOICES
    context['app_modes']=extras.APPLICATION_CHOICES
    if employer_id.payment_verified == True:  
        return render(request,'listings/job_form.html',context)
    else:
        return redirect('subscriptions:initiate-payment')
        
        
def create_job_action(request):

    context = {}
    
    user = CustomUser.objects.get(id=request.user.id)
    employer_id = Employer.objects.get(user_id=user)

    context['user'] = user
    context['employer'] = employer_id
    context['locations'] = extras.LOCATION_CHOICES
    context['countries'] = extras.COUNTRY_CHOICES
    context['job_types'] = extras.JOB_TYPE_CHOICES
    context['experience'] = extras.EXP_CHOICES
    context['qualifications'] = extras.QUALIFICATION_CHOICES
    context['app_modes'] =extras.APPLICATION_CHOICES
    context['title'] ='Create-Job'

    if request.method == 'POST':
        #form = JobForm(request.POST, request.FILES)
        
        company_name=request.POST.get('company_name')
        company_description =request.POST.get('company_description')
        address=request.POST.get('address')
        location=request.POST.get('location')
        country=request.POST.get('country')
        email=request.POST.get('email')
        website=request.POST.get('website')
        title=request.POST.get('title')
        description=request.POST.get('description')
        type=request.POST.get('type')
        qualification = request.POST.get('qualification')
        experience=request.POST.get('experience')
        requirements=request.POST.get('requirements')
        min_salary=request.POST.get('min_salary')
        max_salary=request.POST.get('max_salary')
        application_mode=request.POST.get('application_mode')
        closed_at=request.POST.get('closed_at')
        
        
        if not request.POST.get('published'):
            published=False
        else:
            published = True
            
        

        if employer_id.company_type == 'Direct Employer':
            if not (application_mode and min_salary and max_salary and requirements
                and experience and qualification and type and  description and title
                and country and location and address):
            
                messages.error(request, 'Please provide all the details!!')
                template_name= "listings/job_form.html"
                return render(request,template_name,context)
            else:
                Job.objects.create(created_by=employer_id,
                                    company_name = employer_id.company_name,
                                    company_description=employer_id.company_description,
                                    address=address,
                                    email = employer_id.user_id.email,
                                    website = employer_id.website,
                                    location = location,
                                    country = country,
                                    title=title,
                                    type=type,
                                    qualification = qualification,    
                                    experience=experience,
                                    description=description,
                                    requirements=requirements,
                                    min_salary = min_salary,
                                    max_salary = max_salary,
                                    application_mode=application_mode,
                                    logo=employer_id.logo,
                                    direct_list=True,
                                    is_published=published,
                                    closed_at=closed_at
                                    )
                
                
                messages.success(request, "Job Posted Successfully")
                
                return redirect('/')
            
        else:
            try:
                request.FILES['logo']
            except KeyError:
                messages.error(request, "upload company logo")
                template_name= "listings/job_form.html"
                
                return render(request,template_name,context)
            if not (application_mode and min_salary and max_salary and requirements
                and experience and qualification and type and  description and title
                and country and location and website and email and address and 
                company_description and company_name):
                
            
                messages.error(request, 'Please provide all the details!!')
                template_name= "listings/job_form.html"
                return render(request,template_name,context)
            
            else:
                Job.objects.create(created_by=employer_id,
                                    company_name = company_name,
                                    company_description=company_description,
                                    address=address,
                                    email = email,
                                    website = website,
                                    location = location,
                                    country = country,
                                    title=title,
                                    type=type,
                                    qualification = qualification,    
                                    experience=experience,
                                    description=description,
                                    requirements=requirements,
                                    min_salary = min_salary,
                                    max_salary = max_salary,
                                    application_mode=application_mode,
                                    logo=request.FILES['logo'],
                                    direct_list=False,
                                    is_published=published,
                                    closed_at=closed_at
                                )
                
                messages.success(request, "Job Posted Successfully")
                return redirect('/')
 
    return render(request, 'listings/job_list.html',context)


# 3.Job form update view for employer |
def job_form_update_view(request,slug):
    """
    Handle Job Update
    """
    context = {}
    
    job = None
    if slug is not None:
        try:
            job = Job.objects.get(slug=slug)
            context['job'] = job
        except Job.DoesNotExist:
            raise Http404
        
        context['locations'] = extras.LOCATION_CHOICES
        context['countries'] = extras.COUNTRY_CHOICES
        context['job_types'] = extras.JOB_TYPE_CHOICES
        context['experience'] = extras.EXP_CHOICES
        context['qualifications'] = extras.QUALIFICATION_CHOICES
        context['app_modes'] =extras.APPLICATION_CHOICES
        context['title'] ='Update Job'
        
        
    return render(request,'listings/job_form_update.html',context)


def update_job(request,slug):
    context = {}
    context['locations'] = extras.LOCATION_CHOICES
    context['countries'] = extras.COUNTRY_CHOICES
    context['job_types'] = extras.JOB_TYPE_CHOICES
    context['experience'] = extras.EXP_CHOICES
    context['qualifications'] = extras.QUALIFICATION_CHOICES
    context['app_modes'] =extras.APPLICATION_CHOICES
    context['title'] ='Update Job'
    
    
    try:
        job = Job.objects.get(slug=slug)
        context['job'] = job
    except Job.DoesNotExist:
        raise Http404
    
    if request.method != "POST":
            messages.error(request, "Invalid Method")
            # return redirect('404')
            raise Http404("Job does not exist.")
    else:
        company_name=request.POST.get('company_name')
        company_description=request.POST.get('company_description')
        address=request.POST.get('address')
        email=request.POST.get('email')
        website=request.POST.get('website')
        location=request.POST.get('location')
        country=request.POST.get('country')
        title=request.POST.get('title')
        type=request.POST.get('type')
        qualification = request.POST.get('qualification')
        experience=request.POST.get('experience')
        description=request.POST.get('description')
        requirements=request.POST.get('requirements')
        min_salary=request.POST.get('min_salary')
        max_salary=request.POST.get('max_salary')
        application_mode=request.POST.get('application_mode')
        closed_at=request.POST.get('closed_at')
        #logo =request.FILES['logo']
        

        if not request.POST.get('published'):
            published=False
        else:
            published = True

        if not request.POST.get('published'):
            published=False
        else:
            published = True        
        
        # context= {'locations':extras.LOCATION_CHOICES,
        #       'countries':extras.COUNTRY_CHOICES,
        #       'job_types':extras.JOB_TYPE_CHOICES,
        #       'experience':extras.EXP_CHOICES,
        #       'qualifications':extras.QUALIFICATION_CHOICES,
        #       'app_modes':extras.APPLICATION_CHOICES  
        #       }
        
        if not (closed_at and application_mode and min_salary and max_salary and  requirements and description and 
                    experience and qualification and type and title and country and
                    location and website and email and address and company_description and company_name  ):
                
                
                messages.error(request, 'Please provide all the details!!')
                template_name= "listings/job_form.html"
                return render(request,template_name,context)
        else:
            user = CustomUser.objects.get(id=request.user.id)
            employer_id = Employer.objects.get(user_id=user)

    
            job=Job.objects.get(slug=slug) 
          
            job.created_by = employer_id
            job.company_name = company_name
            job.company_description=company_description
            job.address=address
            job.email = email
            job.website = website
            job.location = location
            job.country = country
            job.title=title
            job.type=type
            job.qualification = qualification    
            job.experience=experience
            job.description=description
            job.requirements=requirements
            job.min_salary = min_salary
            job.max_salary = max_salary
            job.application_mode=application_mode
            # job.logo=logo
            job.is_published = published
            job.closed_at=closed_at
            
            if job.direct_list==True:
                job.logo = employer_id.logo
                job.save()
            else:
                try:
                    request.FILES['logo']
                except KeyError:
                    messages.error(request, "upload company logo")
                    return render(request,'listings/job_form_update.html',context)
                job.logo = request.FILES['logo']
                # job.logo = job.logo
                job.save()
        
            messages.success(request, "Job Updated Successfully")

            return redirect('accounts:employer-direct-job')
    
# Job lists | Done Rem Search...
class JobListView(ListView):
    model = Job
    paginate_by = 10
    context_object_name = 'jobs'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f'Jobs-in-Nigeria {currentYear} Latest-Job-Vacancies-in-Nigeria' 
        context['now'] = timezone.now()
        context["job_counts"] = Job.objects.all().count()
        context['full_time'] = Job.objects.filter(type='Full Time',is_published=True)
        context['remote']=Job.objects.filter(type='Remote',is_published=True)
        context['intership']=Job.objects.filter(type='Intership',is_published=True)
        context['shift']=Job.objects.filter(type='Shift',is_published=True)
        context['published_jobs'] = Job.objects.filter(is_published=True)
        context['featured_jobs'] = Job.objects.filter(is_published=True,direct_list=True)
        context['locations']=extras.LOCATION_CHOICES[1:]
        return context

# Job Detail  |Done  
def job_detail(request,slug=None):
    context = {}
    job = None
    if slug is not None:
        try:
            job = Job.objects.get(slug=slug)
            context['employer'] = job.created_by
        except Job.DoesNotExist:
            raise Http404
    context['job'] = job
    context['recently_list_jobs'] = Job.objects.all()[:5]

    template_name = "listings/job_detail.html"
    return render(request, template_name, context)


# done
@jobseeker_required
def application_form(request,slug=None):
    job = None
    if slug is not None:
        try:
            job = Job.objects.get(slug=slug)
            context={
            'title':'settings',
            'locations':extras.LOCATION_CHOICES,
            'countries':extras.COUNTRY_CHOICES,
            'job_types':extras.JOB_TYPE_CHOICES,
            'experience':extras.EXP_CHOICES,
            'qualifications':extras.QUALIFICATION_CHOICES,
            'numbers':extras.NUMBER_CHOICES,
            'gender':extras.GENDER_CHOICES,
            'booleann':extras.BOOLEAN_CHOICES,
            'job':job
              }
        except Job.DoesNotExist:
            messages.error(request, 'job does not exit')
            raise Http404
        
        
        user = CustomUser.objects.get(id=request.user.id)
        jobseeker = JobSeeker.objects.get(user_id=user)
        job = Job.objects.get(slug=slug)
        context={
            'title':'settings',
            'locations':extras.LOCATION_CHOICES,
            'countries':extras.COUNTRY_CHOICES,
            'job_types':extras.JOB_TYPE_CHOICES,
            'experience':extras.EXP_CHOICES,
            'qualifications':extras.QUALIFICATION_CHOICES,
            'numbers':extras.NUMBER_CHOICES,
            'gender':extras.GENDER_CHOICES,
            'booleann':extras.BOOLEAN_CHOICES,
            'users':user,
            'jobseeker':jobseeker,
            'job':job
              }
            
            # check is users has already applied
        if Applicant.objects.filter(job_id=job.id,jobseeker_id=jobseeker): 
            messages.error(request, "Already applied!")
            return redirect('listings:home')    
        else:
            template_name = "listings/job_application_form.html"
            return render(request,template_name,context)
    
        
        

# application             
@login_required(login_url='accounts:login')
def apply(request,slug=None):
    if not request.user.user_type==CustomUser.JOBSEEKER:
        raise PermissionDenied
    
    context= {'title':'Apply',
              'locations':extras.LOCATION_CHOICES,
              'countries':extras.COUNTRY_CHOICES,
              'job_types':extras.JOB_TYPE_CHOICES,
              'experience':extras.EXP_CHOICES,
              'qualifications':extras.QUALIFICATION_CHOICES,
              'numbers':extras.NUMBER_CHOICES,
              'gender':extras.GENDER_CHOICES,
              'booleann':extras.BOOLEAN_CHOICES,
              }
    job = None
    if slug  is not None:
        try:
            job = Job.objects.get(slug=slug)
            context['job'] = job
        except Job.DoesNotExist:
            raise Http404
        except Job.MultipleObjectsReturned:
            job = Job.objects.get(slug=slug)
        except:
            raise Http404
        
    
    if request.method =='POST':
        
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        gender= request.POST.get('gender')
        address= request.POST.get('address')
        location= request.POST.get('location')
        country= request.POST.get('country')
        experience = request.POST.get('experience')
        qualification = request.POST.get('qualification')
        cover_letter = request.POST.get('cover_letter')
        portfolio_link = request.POST.get('portfolio_link')
        resume = request.FILES['resume']
        
        
        
        if not(resume and portfolio_link and cover_letter 
               and qualification and experience and country 
               and location and address and gender and phone_number 
               and email and last_name and first_name ):
            
            
            messages.error(request, 'Please provide all the details!!')
            template_name= "listings/job_application_form.html"
            return render(request,template_name,context)
        else:
            try:
                user = CustomUser.objects.get(id=request.user.id)
                jobseeker = JobSeeker.objects.get(user_id=user)
                
               
                # check is users exists
                if Applicant.objects.filter(job_id=job.id,jobseeker_id=jobseeker):
                
                    messages.error(request, "Already applied!")
                    return redirect('listings:home')    
                else:
                    # create new instance of CustomeUser()
                    Applicant.objects.create(
                    job_id=job,
                    jobseeker_id=jobseeker,
                    first_name = first_name,
                    last_name = last_name,
                    email = email,
                    phone_number = phone_number,
                    gender = gender,
                    experience=experience,
                    qualification=qualification,
                    portfolio_link=portfolio_link,
                    address=address,
                    location=location,
                    country=country,
                    resume=resume,
                    cover_letter=cover_letter
                    )
                    
                    # Send email...
                    # messages.success(request, "Successfully registered")
                    #link = request.build_absolute_uri(reverse('accounts:login'))

                    template_name='accounts/html_email_templates/application_submitted.html'
                    subject='Application submitted'
                    email_to=user.email
                    content={'support_team_name':extras.support_team_name,
                            'version':extras.version,
                            #'link':link,
                            'job':job,
                            'user':user,
                            }
                    # email to candidate
                    msg = "Successfully registered"
                    extras.send_html_email(request,template_name,content,subject,email_to,msg)
                    
                    #email to employer
                    template_name='accounts/html_email_templates/application_submitted.html'
                    subject='New Applicant'
                    email_to=job.created_by.user_id.email
                    content={'support_team_name':extras.support_team_name,
                            'version':extras.version,
                            #'link':link,
                            'job':job,
                            'user':user,
                            'cover_letter':cover_letter,
                            }
                    mail = EmailMessage(subject, cover_letter, settings.EMAIL_HOST_USER, [email_to])
                    mail.attach(resume.name, resume.read(), resume.content_type)
                    mail.send()
                    
                    messages.success(request, 'Your application has been submitted successfully.')
                    return redirect('listings:home')  
            except Job.DoesNotExist:
                raise Http404          
    else:
        messages.error(request,'Bad form format')
        return redirect('404')



# search job by location
def search_job_by_location(request):
    context = {}
    if request.method =="POST":
        location= request.POST.get('location')
        if location:
            jobs_by_location = Job.objects.filter(Q(location__contains=location,is_published=True))
            context['jobs_by_location']=jobs_by_location
            context['locations']=extras.LOCATION_CHOICES[1:]
            return render(request,'listings/jobs_by_location.html',context=context)
            
    
    context['full_time'] = Job.objects.filter(type='Full Time')[:5]
    context['part_time']=Job.objects.filter(type='Part Time')[:5]
    context['remote']=Job.objects.filter(type='Remote')[:5]
    context['intership']=Job.objects.filter(type='Intership')[:5]
    context['featured_job']=Job.objects.filter(type='Featured job')[:5]
    context['locations']=extras.LOCATION_CHOICES[1:]
    context['title']='Find-job-by-location'
    return render(request,'listings/jobs_by_location.html',context=context)
   
    

# search job by location and company_name|job_title
def search_job_by_location_keyword(request):
    if request.method =="POST":
        location= request.POST.get('location')
        search_comName_comTitle= request.POST.get('search_comName_comTitle')
        jobs = Job.objects.all()
        if location:
            job_filter = jobs.filter(Q(location__contains=location,is_published=True))
            context = {'job_filter':job_filter,
                    'locations':extras.LOCATION_CHOICES[1:],}
            return render(request,'listings/job_list.html',context)
            
        elif search_comName_comTitle:
            job_filter = jobs.filter(Q(company_name__contains=search_comName_comTitle,is_published=True) | Q(title__contains=search_comName_comTitle,is_published=True))

            context = {'job_filter':job_filter,
                    'locations':extras.LOCATION_CHOICES[1:],}
            return render(request,'listings/job_list.html',context)
        else:
            context = {
                    'locations':extras.LOCATION_CHOICES[1:],}
            messages.error(request, "Select a location or type in the comapany name or job title to find a job")
            return render(request,'listings/job_list.html',context)
 

# delete job   
@login_required(login_url='accounts:login')
def delete_job(request,slug):    
    job=Job.objects.filter(slug=slug)
    job.delete()
    return redirect('accounts:employer-direct-job')
    




