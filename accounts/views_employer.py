from django.shortcuts import render, redirect , get_object_or_404
from accounts.models import *
from django.contrib import messages
from django.http import Http404
from core import extras
from django.contrib.auth import login,logout
from django.views.decorators.csrf import csrf_exempt
from accounts.forms import *
from listings.models import *
from subscriptions.models import Payment
from django.contrib.auth.decorators import login_required
from listings.decorators import *


@login_required(login_url='accounts:login')
# @employer_required
def dashboard(request):
    context={}
    user = get_object_or_404(CustomUser, id=request.user.id)
    #user = CustomUser.objects.get(id=request.user.id)
    employer = Employer.objects.get(user_id=user)
    jobs_by_employer = Job.objects.filter(created_by=employer)
    context['jobs'] = jobs_by_employer
    context['job_count'] = Job.objects.filter(created_by=employer).count()
    context['indirect_list_count'] = Job.objects.filter(created_by=employer,direct_list=False).count()
    context['direct_list_count'] = Job.objects.filter(created_by=employer,direct_list=True).count()
    context['applicants_count'] = Applicant.objects.filter(job_id__created_by=employer).count()
    template_name = "accounts/employer/dashboard.html"
    return render(request,template_name,context)
        

@login_required(login_url='accounts:login')  
def settings(request):
    
    context = {}

    try:
        user = CustomUser.objects.get(id=request.user.id)
        employer = Employer.objects.get(user_id=user)
        payments = Payment.objects.filter(payment_by=employer) # New to be effect in next vesion
        context = {'user':user,'employer':employer,}
    except CustomUser.DoesNotExist:
        raise Http404("User does not exist.") 
    context['title']='settings'
    context['user']=user
    context['employer']=employer
    context['locations']=extras.LOCATION_CHOICES
    context['countries']=extras.COUNTRY_CHOICES
    context['company_types']=extras.COMPANY_TYPE_CHOICES
    context['industries']=extras.INDUSTRY_CHOICES
    context['numbers']=extras.NUMBER_CHOICES
    context['payments'] = payments.order_by('-created_date') # New to be effect in next vesion
    context['current_payment'] = payments.last() # New to be effect in next vesion
              
    
    template_name = 'accounts/employer/settings.html'
    return render(request,template_name,context)
        

def update_settings(request):
    context = {}
    try:
        user = CustomUser.objects.get(id=request.user.id)
        employer = Employer.objects.get(user_id=user)
        context['user']=user
        context['employer']=employer
        if request.method != "POST":
            raise Http404("Bad format.")
        else:
            company_name= request.POST.get('company_name')
            company_industry= request.POST.get('company_industry')
            company_type= request.POST.get('company_type')
            address= request.POST.get('address')
            location= request.POST.get('location')
            country= request.POST.get('country')
            number_of_employees= request.POST.get('number_of_employees')
            website= request.POST.get('website')
            company_description= request.POST.get('company_description')
            
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email').lower()
            phone_number = request.POST.get('phone_number')
            
            if not (company_name and company_industry and company_type and address and
                    location and country and number_of_employees and website and company_description
                    and first_name and last_name and email and phone_number
                    ):
                context={   'user':user, 'employer':employer,
                            'title':'settings',
                            'locations':extras.LOCATION_CHOICES,
                            'countries':extras.COUNTRY_CHOICES,
                            'company_types':extras.COMPANY_TYPE_CHOICES,
                            'industries':extras.INDUSTRY_CHOICES,
                            'numbers':extras.NUMBER_CHOICES
                        }
                
                messages.error(request, 'Please provide all the details!!')
                template_name = 'accounts/employer/settings.html'
                return render(request,template_name,context)
            else:
                employer.company_name=company_name
                employer.company_industry=company_industry
                employer.company_type = company_type
                employer.address=address
                employer.location=location
                employer.country=country
                employer.number_of_employees=number_of_employees
                employer.website=website
                employer.company_description=company_description
                employer.save()
                
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.phone_number = phone_number
                user.save()
                
                messages.success(request, "Company Profile Updated Successfully")
                return redirect('accounts:employer-settings')
    except CustomUser.DoesNotExist:
        raise Http404("User does not exist.")


def update_logo(request):
    max_upload_limit = 2*1024*1024 # 2mb # image size lime to effect in next version
    if request.method == 'POST':
        
        try:
            request.FILES['logo']
            employer = get_object_or_404(Employer,user_id=request.user.id)
            
            employer.logo = request.FILES['logo'] 

            employer.save()
            messages.success(request, "Company logo Updated Successfully")
            return redirect('accounts:employer-settings') 
        except KeyError:
            messages.error(request, "select a file")
            return redirect('accounts:employer-settings')
   
def remove_logo(request):

    employer = get_object_or_404(Employer,user_id=request.user.id)
    if employer.logo == 'default.png':
        messages.error(request, "file is empty")
        return redirect('accounts:employer-settings') 
    else:
        employer.logo.delete(save=False) # delete old image file
        employer.logo = 'default.png'
        employer.save()
        messages.success(request, "Company logo removed successfully")
        
        return redirect('accounts:employer-settings')

@login_required(login_url='accounts:login')   
def profile(request):
    template_name= template_name = "accounts/employer/profile.html"
    context={'title':'Profile'}
    return render(request,template_name,context)
    
@login_required(login_url='accounts:login') 
def billing(request):
    context = {}
    employer_id = Employer.objects.get(user_id=request.user.id)
    payments = Payment.objects.filter(payment_by=employer_id)
    context['title'] ='Billings'
    context['employer'] =employer_id
    context['payments'] = payments.order_by('-created_date')
    context['current_payment'] = payments.last()
    template_name = "accounts/employer/billing.html"
    return render(request,template_name,context)

@login_required(login_url='accounts:login')
def security(request):
    
    user = CustomUser.objects.get(id=request.user.id)
    employer=Employer.objects.get(user_id=user)
    context={'title':'Security',
            'users':user,
             'employer':employer
            }
    template_name= template_name = "accounts/employer/security.html"
    return render(request,template_name,context)

def update_password(request):
    if request.method=='POST':
    
        if request.POST.get('new_password') != request.POST.get('confirm_password'):
            messages.error(request, 'Password and confirm password does not match')
            return redirect('accounts:employer-security')
        else:
            try:
                user = CustomUser.objects.get(id=request.user.id)
                #user.password = make_password(new_password)
                #employer = Employer.objects.get(user_id=user)
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
        return redirect('accounts:employer-security')

    try:
        user = CustomUser.objects.get(id=request.user.id)
        if CustomUser.objects.filter(username=new_username).exists():
            messages.error(request, 'Username is already taken. Please use different username')
            return redirect('accounts:employer-security')
        else:
            user.username = new_username
            user.save()
            login(request, user)
            messages.success(request, "Username Updated Successfully")
            return redirect('accounts:employer-security')
    
    except CustomUser.DoesNotExist:
        raise Http404("User does not exist.")
 
@login_required(login_url='accounts:login')   
def indirect_job(request):
    user = get_object_or_404(CustomUser, id=request.user.id)
    #user = CustomUser.objects.get(id=request.user.id)
    employer = Employer.objects.get(user_id=user)
    indirect_list = Job.objects.filter(created_by=employer,direct_list=False)
    indirect_list_count = Job.objects.filter(created_by=employer,direct_list=False).count()

    template_name="accounts/employer/indirect_list.html"   
    context={"employer":employer,
             "indirect_list":indirect_list,
             "indirect_list_count":indirect_list_count,
             "title":'Featured Listing',}
    
    return render(request,template_name=template_name,context=context)

@login_required(login_url='accounts:login')
def direct_job(request):
    user = CustomUser.objects.get(id=request.user.id)
    employer = Employer.objects.get(user_id=user)
    direct_list = Job.objects.filter(created_by=employer,direct_list=True)
    direct_list_count = Job.objects.filter(created_by=employer,direct_list=True).count()

    template_name="accounts/employer/direct_list.html"   
    context={"employer":employer,
             "direct_list":direct_list,
             "direct_list_count":direct_list_count,
             "title":'Direct Listing',}
    
    return render(request,template_name=template_name,context=context)

@login_required(login_url='accounts:login')
def applicants(request):
    employer = Employer.objects.get(user_id=request.user.id)
    applicants = Applicant.objects.filter(job_id__created_by=employer)
    applicants_count = Applicant.objects.filter(job_id__created_by=employer).count()

    template_name="accounts/employer/applicants.html"   
    context={'applicants':applicants,
             'title':'Applicants',
             'applicants_count':applicants_count}
    
    return render(request,template_name,context)

@login_required(login_url='accounts:login')
def notification(request): 
    user = CustomUser.objects.get(id=request.user.id)
    instance = get_object_or_404(Employer, user_id=user)
    form = NotificationEmployerForm(request.POST or None, instance=instance)
   
    if form.is_valid():
        form.save()
        return redirect('accounts:employer-notification')

    template_name = "accounts/employer/notification.html"
    return render(request,template_name, {'form':form,'title':'Notifications'})

@login_required(login_url='accounts:login')            
def employer_feedback(request):
  return render(request, "employer/feedback.html")
 
 
def employer_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('employer_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        employer_obj = Employer.objects.get(user_id=request.user.id)
 
        try:
            add_feedback = FeedBackEmployer(staff_id=employer_obj,
                                          feedback=feedback,
                                          feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('employer_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('employer_feedback')
        
@login_required(login_url='accounts:login')     
def delete_account(request):
   
    if request.method == "POST":
        employer = Employer.objects.get(user_id=request.user.id)
    
        if employer.check_password(request.POST.get("password")):
            del request.session['is_jobseeker']
            employer.delete()
            logout(request)
            messages.success(request, "Account deleted successfully")
            return redirect('/')
        else:
            messages.error(request, 'Inccorect password!')
            return redirect("accounts:employer-security")