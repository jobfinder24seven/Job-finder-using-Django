from django.shortcuts import render,redirect
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin 
from accounts.models import *
from accounts.forms import *
from django.contrib import messages
from django.http import Http404
from core import extras
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from accounts.models import JobSeeker
from listings.models import Job,Applicant
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
   
class JobSeekerHomeView(LoginRequiredMixin,TemplateView):
    #optional
    login_url = "accounts:login"
    raise_exception = False

    template_name = "accounts/jobseeker/dashboard.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Dashboard' 
        context['jobs'] = Job.objects.filter(is_published=True)
        return context

@login_required(login_url='accounts:login')     
def manage_job(request):
    template_name= template_name = "accounts/employer/profile.html"
    context={'title':'settings'}
    return render(request,template_name,context)

@login_required(login_url='accounts:login')   
def profile(request):
    template_name= template_name = "accounts/employer/profile.html"
    context={'title':'Profile'}
    return render(request,template_name,context)

@login_required(login_url='accounts:login')
def settings(request):
    
    try:
        user = CustomUser.objects.get(id=request.user.id)
        jobseeker = JobSeeker.objects.get(user_id=user)
        context = {'user':user,'jobseeker':jobseeker,}
    except CustomUser.DoesNotExist:
        #raise Http404("User does not exist.")
        messages.error(request, 'Invalid Credentials!!')
        return redirect('404')  
    context={
            'title':'Profile',
            'locations':extras.LOCATION_CHOICES,
            'countries':extras.COUNTRY_CHOICES,
            'job_types':extras.JOB_TYPE_CHOICES,
            'experience':extras.EXP_CHOICES,
            'qualifications':extras.QUALIFICATION_CHOICES,
            'numbers':extras.NUMBER_CHOICES,
            'gender':extras.GENDER_CHOICES,
            'booleann':extras.BOOLEAN_CHOICES,
            'user':user,
            'jobseeker':jobseeker,
              }
    
    template_name = 'accounts/jobseeker/settings.html'
    return render(request,template_name,context)
        

def update_settings(request):
    try:
        user = CustomUser.objects.get(id=request.user.id)
        jobseeker = JobSeeker.objects.get(user_id=user)
      
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
             'user':user,
             'jobseeker':jobseeker,
              }
        if request.method != "POST":
            messages.error(request, "Invalid Method")
            return redirect('404')
            #raise Http404("User does not exist.")
        else:
            gender= request.POST.get('gender')
            dob= request.POST.get('dob')
            address= request.POST.get('address')
            location= request.POST.get('location')
            country= request.POST.get('country')
            summary = request.POST.get('summary')
            education= request.POST.get('education')
            experience= request.POST.get('experience')
            education= request.POST.get('education')
            skills= request.POST.get('skills')
            portfolio_link=request.POST.get('portfolio_link')
         
            
            #resume= request.FILES['resume']
            # avater= request.POST.get('avater')
            display_resume_yes_no= request.POST.get('display_resume')
            
            min_salary= request.POST.get('min_salary')
            max_salary= request.POST.get('max_salary')
            job_type= request.POST.get('job_type')
            
            
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email').lower()
            phone_number = request.POST.get('phone_number')
            
           
            if not (gender and dob and address and
                    location and country and summary  
                    and experience and education
                    and skills and portfolio_link 
                    and display_resume_yes_no and min_salary and max_salary and job_type
                    and first_name and last_name and email and phone_number
                    ):
                
                messages.error(request, 'Please provide all the details!!')
                template_name = 'accounts/jobseeker/settings.html'
                return render(request,template_name,context)
            else:
                if display_resume_yes_no == '-':
                    display_resume = False
                elif display_resume_yes_no == 'NO':
                    display_resume = False
                elif display_resume_yes_no == 'YES':
                    display_resume = True
                
                
                jobseeker.dob= dob
                jobseeker.address = address
                jobseeker.location = location
                jobseeker.country = country
                jobseeker.summary = summary
                jobseeker.experience = experience
                jobseeker.education = education
                jobseeker.skills = skills
                jobseeker.portfolio_link = portfolio_link
               # jobseeker.resume = resume
                jobseeker.display_resume=display_resume
                jobseeker.min_salary=min_salary
                jobseeker.max_salary = max_salary
                jobseeker.job_type = job_type
                jobseeker.save()
                
                
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.phone_number = phone_number
                user.gender = gender
                user.save()
                
                messages.success(request, "Profile Updated Successfully")
                return redirect('accounts:jobseeker-settings')
    
    except CustomUser.DoesNotExist:
        # raise Http404("User does not exist.")
        messages.error(request, 'Invalid Credentials!!')
        return redirect('404')    

@login_required(login_url='accounts:login')
def manage_job(request):
    
    user = CustomUser.objects.get(id=request.user.id)
    jobseeker = JobSeeker.objects.get(user_id=user)
    try:
        list_jobs = Job.objects.filter(is_published=True)
        list_jobs_count = Job.objects.all().count()
        applicant = Applicant.objects.filter(jobseeker_id=jobseeker)
        template_name="accounts/jobseeker/manage_jobs.html"   
        context={"list_jobs":list_jobs,"list_job_count":list_jobs_count,'applicant':applicant}
    except Applicant.DoesNotExist:
        
        template_name="accounts/jobseeker/manage_jobs.html"   
        context={"list_jobs":list_jobs,
                 "list_job_count":list_jobs_count,
                 "title":"Manage Jobs"}
      
    
    return render(request,template_name,context)

def update_avater(request):
    if request.method == 'POST':
        
        try:
            request.FILES['avater']  
            try:
                user = CustomUser.objects.get(id=request.user.id)
                jobseeker = JobSeeker.objects.get(user_id=user)
                jobseeker.avater = request.FILES['avater'] 
                jobseeker.save()
                messages.success(request, "Profile Pics. Updated Successfully")
                
                return redirect('accounts:jobseeker-settings')  
            except CustomUser.DoesNotExist:
                raise Http404("User does not exist.")
        except KeyError:
            messages.error(request, "select a file")
            return redirect('accounts:jobseeker-settings')
   
def remove_avater(request):
    try:
        user = CustomUser.objects.get(id=request.user.id)
        jobseeker = JobSeeker.objects.get(user_id=user)
        if jobseeker.avater== 'default.png':
            messages.error(request, "file is empty")
            return redirect('accounts:jobseeker-settings') 
        else:
            jobseeker.avater.delete(save=False) # delete old image file
            jobseeker.avater = 'default.png'
            jobseeker.save()
            messages.success(request, "Profile picture removed successfully")
        
            return redirect('accounts:jobseeker-settings')  
    except CustomUser.DoesNotExist:
        raise Http404("User does not exist.")
   

@login_required(login_url='accounts:login')
def security(request):
    template_name= template_name = "accounts/jobseeker/security.html"
    user = CustomUser.objects.get(id=request.user.id)
    jobseeker=JobSeeker.objects.get(user_id=user)
    context={'title':'security',
            'users':user,
             'jobseeker':jobseeker
            }
    return render(request,template_name=template_name,context=context)

def update_password(request):
    if request.method=='POST':
    
        if request.POST.get('new_password') != request.POST.get('confirm_password'):
            messages.error(request, 'Password and confirm password does not match')
            return redirect('accounts:jobseeker-security')
        else:
            try:
                user = CustomUser.objects.get(id=request.user.id)
                #user.password = make_password(new_password)
                user.set_password(request.POST.get('new_password'))
                user.save()
                logout(request)
                messages.success(request, "Password Updated Successfully")
                return redirect('accounts:login')
            
            except CustomUser.DoesNotExist:
                raise Http404("User does not exist.")
    
@csrf_exempt
def update_username(request):
    if request.method=='POST':
        new_username= request.POST.get('new_username')

    if not(new_username):
        messages.error(request, "provide enter username")
        return redirect('accounts:jobseeker-security')

    try:
        user = CustomUser.objects.get(id=request.user.id)
        if CustomUser.objects.filter(username=new_username).exists():
            messages.error(request, 'Username is already taken. Please use different username')
            return redirect('accounts:jobseeker-security')
        else:
            user.username = new_username
            user.save()
            # login(request, user)
            messages.success(request, "Username Updated Successfully")
            return redirect('accounts:jobseeker-security')
    
    except CustomUser.DoesNotExist:
        raise Http404("User does not exist.")

@login_required(login_url='accounts:login')
def notification(request): 
    user = CustomUser.objects.get(id=request.user.id)
    instance = get_object_or_404(JobSeeker, user_id=user)
    
    form = NotificationJobSeekerForm(request.POST or None, instance=instance)
   
    if form.is_valid():
        form.save()
        return redirect('accounts:jobseeker-notification')

    template_name = "accounts/jobseeker/notification.html"
    return render(request,template_name, {'form':form})
    
@login_required(login_url='accounts:login')
def delete_account(request):
    user = CustomUser.objects.get(pk=request.user.id)
    del request.session['is_jobseeker']
    user.delete()
    logout(request)
    
    messages.success(request, "Account deleted successfully")
    return redirect('/')


@login_required(login_url='accounts:login')
def upload_cv(request):
    try:
        user = CustomUser.objects.get(id=request.user.id)
        jobseeker=JobSeeker.objects.get(user_id=user)
        context={'users':user,'jobseeker':jobseeker
        }
        template_name = 'accounts/jobseeker/upload_cv.html'
        return render(request,template_name,context)
    except CustomUser.DoesNotExist:
            messages.error(request, 'Invalid Credentials!!')
            return redirect('404')

def update_cv(request):
    resume = request.FILES["resume"]
    if resume == '':
        messages.error(request, "select resume")
        return redirect('accounts:jobseeker-cv-update')
    try:
        user = CustomUser.objects.get(id=request.user.id)
        jobseeker=JobSeeker.objects.get(user_id=user)
        jobseeker.resume = resume
        jobseeker.save()
        messages.success(request, "Resume uploaded Successfully")
        return redirect('accounts:jobseeker-home')  
    except CustomUser.DoesNotExist:
            messages.error(request, 'Invalid Credentials!!')
            return redirect('404')
        
@login_required(login_url='accounts:login')
def jobseeker_feedback(request):
    jobseeker_obj = JobSeeker.objects.get(user_id=request.user.id)
    feedback_data = FeedBackJobSeeker.objects.filter(jobseeker_id=jobseeker_obj)
    context = {
        "feedback_data": feedback_data
    }
    return render(request, 'jobseeker/feedback.html', context)
 
@login_required(login_url='accounts:login')
def jobseeker_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('jobseeker_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        jobseeker_obj = JobSeeker.objects.get(user_id=request.user.id)
 
        try:
            add_feedback = FeedBackJobSeeker(jobseeker_id=jobseeker_obj,
                                           feedback=feedback,
                                           feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('jobseeker_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('jobseeker_feedback')


    
    
