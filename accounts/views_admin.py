from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic.base import TemplateView
from accounts.models import *
from subscriptions.models import *
from listings.models import *
from main.models import *
from main.forms import *
from core import extras
from django.http import Http404
from django.contrib.auth.hashers import make_password,check_password
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from subscriptions.forms import *
import datetime
from dateutil import relativedelta
    
class AdminHomeView(LoginRequiredMixin,TemplateView):
    #optional
    login_url = "login-admin"
    # redirect_field_name = "hollaback"
    raise_exception = False
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = CustomUser.objects.all()
        context['jobseeker_list'] = CustomUser.objects.filter(user_type=CustomUser.JOBSEEKER)
        context['employer_list'] = Employer.objects.all()
        context['user_count'] = CustomUser.objects.all().count()
        context['employer_list_count'] = Employer.objects.all().count()
        context['jobseeker_list_count'] = JobSeeker.objects.all().count()
        context['newsletter_subscriber_list_count'] = NewsletterSubscriber.objects.all().count()
        context['payment_count'] = Payment.objects.all().count()
        return context

    template_name = "accounts/admin/dashboard.html"

# Admin Dashboard
@login_required(login_url='login-admin')    
def dashboard(request):
    context={}
    
    employer_list = CustomUser.objects.filter(user_type=CustomUser.EMPLOYER)
    context['employers']= employer_list
    template_name="accounts/admin/dashborad.html"   
    
    return render(request,template_name,context)

@login_required(login_url='login-admin') 
def employer_list(request):
    context={}

    context['users'] = CustomUser.objects.all()
    context['user_count'] = CustomUser.objects.all().count()
    context['employer_list'] = Employer.objects.all()
    context['employer_list_count'] = Employer.objects.all().count()
    context['jobseeker_list_count'] = JobSeeker.objects.all().count()
    context['payment_count'] = Payment.objects.all().count()
    template_name="accounts/admin/employer_list.html"   
    return render(request,template_name,context)

@login_required(login_url='login-admin') 
def employer_profile(request,slug):    
    context = {}
    
    employer = None
    if slug is not None:
        try:
            employer = Employer.objects.get(slug=slug)
            # show payments history for each users
            payments = Payment.objects.filter(payment_by=employer)
            
            # show current payment
            #payment = payments.last()

            # pass datas to context 
            context['payment'] = payments
            context['employer'] = employer
            context['user'] = employer.user_id

        except Employer.DoesNotExist:
            raise Http404('User does not exist')
    return render(request,'accounts/admin/employer_profile.html',context)

@login_required(login_url='login-admin') 
def employer_payments(request,slug):
    
    context = {}
    
    employer = None
    if slug is not None:
        try:
            employer_id = Employer.objects.get(slug=slug)
            # show payments history for each users
            payments = Payment.objects.filter(payment_by=employer_id)
            
            
            # show current payment
            # payment = payments.last()

            # pass datas to context 
            context['payment'] = payments
            context['employer_id'] = employer_id
            context['payments'] = payments.order_by('-created_date')
            context['user'] = employer_id.user_id

        except Employer.DoesNotExist:
            raise Http404('User does not exist')
    return render(request,'accounts/admin/employer_payments.html',context)


@login_required(login_url='login-admin') 
def verify_payment_page(request,ref):
    context = {}
    if ref is not None:
        try:
            payment = Payment.objects.get(ref=ref)
            employer = Employer.objects.get(slug=payment.payment_by.slug)
            if payment:
                context['payment'] = payment
                context['employer'] = employer
                template_name = "accounts/admin/employer_payments_verify_page.html"
                return render(request, template_name, context)
            
        except Payment.DoesNotExist:
            raise Http404

@login_required(login_url='login-admin') 
def verify_payment(request,ref):    
    if ref is not None:
        try:
            payment = Payment.objects.get(ref=ref)
            employer = Employer.objects.get(slug=payment.payment_by.slug)
            number_of_month = int(request.POST.get('month'))
            if int(request.POST.get('verified')) == 1:
                payment.verified=True
                employer.payment_verified=True
                employer.next_payment_date = datetime.date.today() + relativedelta.relativedelta(months=int(number_of_month))
                payment.save()
                employer.save()
                
                messages.success(request,'Successfuly verified')
            else:
                payment.verified  = False
                employer.payment_verified=False
                employer.next_payment_date = ''
                payment.save()
                employer.save()
                messages.success(request,'Successfuly updated')
            return redirect(reverse('verify-payment-page', kwargs={'ref':payment.ref}))

        except Payment.DoesNotExist:
            raise Http404   


# Jobseeker features
@login_required(login_url='login-admin')         
def jobseeker_list(request):
    context={}

    context["jobseeker_list"] = JobSeeker.objects.all()
    context["jobseeker_list_count"]=JobSeeker.objects.all().count()
    
    template_name="accounts/admin/jobseeker_list.html" 
    return render(request,template_name,context)

@login_required(login_url='login-admin') 
def jobseeker_profile(request,slug):    
    context = {}
    
    jobseeker = None
    if slug is not None:
        try:
            jobseeker = JobSeeker.objects.get(slug=slug)

            context['jobseeker'] = jobseeker
            context['user'] = jobseeker.user_id

        except JobSeeker.DoesNotExist:
            raise Http404('User does not exist')
    return render(request,'accounts/admin/jobseeker_profile.html',context)


@login_required(login_url='accounts:login')
def create_newsletter(request): 
    return render(request,'accounts/admin/newsletter_form.html')

def push(request,newsletter,subject,body,content,email_to):
    template_name='accounts/html_email_templates/newsletter.html'
    if int(request.POST['status'])==0:
                newsletter.body = body
                newsletter.subject = subject
                newsletter.status = int(request.POST['status'])
                newsletter.email_to = int(request.POST['account'])
                messages.success(request, 'saved')
                newsletter.save()
    elif int(request.POST['status']) == 1:
                newsletter.body = body
                newsletter.subject = subject
                newsletter.status = int(request.POST['status'])
                newsletter.email_to = int(request.POST['account'])
                newsletter.save()
                msg = "mail sent"
                extras.send_html_email(request,template_name,content,subject,email_to,msg)
    return redirect('create-newsletter')  

def newsletter_action(request):
    newsletter = Newsletter()
    newsletter_sub = NewsletterSubscriber.objects.all()
    employers = Employer.objects.all()
    jobseekers = JobSeeker.objects.all()
    employers_newsletter_sub = Employer.objects.filter(subscribed_to_newsletter=True)
    jobseekers_newsletter_sub = JobSeeker.objects.filter(subscribed_to_newsletter=True)
    
    # send_email
    if request.method == 'POST':
        subject = request.POST['subject']
        body = request.POST['body']
        
        content={'support_team_name':extras.support_team_name,
                'version':extras.version,
                'body':body
                    }
        if int(request.POST['account']) == 1:
            pass
        
        # email_to_employers_main_account
        elif int(request.POST['account']) == 2:
            email_to = [e.user_id.email for e in employers]
            return push(request,newsletter,subject,body,content,email_to)
              
        # email_to_jobseekers_main_account
        elif int(request.POST['account']) == 3:
            email_to = [e.user_id.email for e in jobseekers]
            return push(request,newsletter,subject,body,content,email_to)
            
        # email_to_employers_subscribed_to_newsletter
        elif int(request.POST['account']) == 4:
            email_to = [e.user_id.email for e in employers_newsletter_sub]
            return push(request,newsletter,subject,body,content,email_to)
        
        # email_to_jobseeker_subscribe_to_newsletter 
        elif int(request.POST['account']) == 5:
            email_to = [e.user_id.email for e in jobseekers_newsletter_sub]
            return push(request,newsletter,subject,body,content,email_to)
        
        # email_to_not_a_member_newsletter_account 
        elif int(request.POST['account']) == 6:
            email_to = [e.email for e in newsletter_sub]
            return push(request,newsletter,subject,body,content,email_to)

@login_required(login_url='accounts:login')
def newsletter_view(request): 
    newsletters = Newsletter.objects.all()
    for n in newsletters:
        print(type(n.email_to))
    newsletter_count = Newsletter.objects.all().count()
    return render(request,'accounts/admin/newsletter_view.html',{'newsletters':newsletters,
                                                                 'newsletter_count':newsletter_count})

@login_required(login_url='accounts:login')
def newsletter_update_view(request,slug): 
    newsletter = Newsletter.objects.get(slug=slug)
    return render(request,'accounts/admin/newsletter_form_update.html',{'newsletter':newsletter})

@login_required(login_url='accounts:login')
def newsletter_update_action(request,slug): 
    newsletter = Newsletter.objects.get(slug=slug)
    newsletter_sub = NewsletterSubscriber.objects.all()
    employers = Employer.objects.all()
    jobseekers = JobSeeker.objects.all()
    employers_newsletter_sub = Employer.objects.filter(subscribed_to_newsletter=True)
    jobseekers_newsletter_sub = JobSeeker.objects.filter(subscribed_to_newsletter=True)
    
    # send_email
    if request.method == 'POST':
        subject = request.POST['subject']
        body = request.POST['body']
        
        content={'support_team_name':extras.support_team_name,
                'version':extras.version,
                'body':body
                    }
        if int(request.POST['account']) == 1:
            pass
        
        # email_to_employers_main_account
        elif int(request.POST['account']) == 2:
            email_to = [e.user_id.email for e in employers]
            return push(request,newsletter,subject,body,content,email_to)
              
        # email_to_jobseekers_main_account
        elif int(request.POST['account']) == 3:
            email_to = [e.user_id.email for e in jobseekers]
            return push(request,newsletter,subject,body,content,email_to)
            
        # email_to_employers_subscribed_to_newsletter
        elif int(request.POST['account']) == 4:
            email_to = [e.user_id.email for e in employers_newsletter_sub]
            return push(request,newsletter,subject,body,content,email_to)
        
        # email_to_jobseeker_subscribe_to_newsletter 
        elif int(request.POST['account']) == 5:
            email_to = [e.user_id.email for e in jobseekers_newsletter_sub]
            return push(request,newsletter,subject,body,content,email_to)
        
        # email_to_not_a_member_newsletter_account 
        elif int(request.POST['account']) == 6:
            email_to = [e.email for e in newsletter_sub]
            return push(request,newsletter,subject,body,content,email_to)
    return redirect('newsletter-view')


@login_required(login_url='login-admin') 
def manage_job(request):
    return render(request, 'accounts/admin/listing.html',{'listings':Job.objects.filter(is_published=True)})

@login_required(login_url='login-admin') 
def delete_job(request, slug):
    job = Job.objects.get(slug=slug)
    try:
        job.delete()
        messages.success(request, "Job Deleted Successfully.")
        return redirect('admin-manage-listing')
    except:
        messages.error(request, "Failed to Delete Course.")
        return redirect('admin-manage-listing')



# Utilities
def create_admin(request):
    user_type = 10/10
    new_user = CustomUser()
    new_user.user_type = user_type
    new_user.username=extras.username_
    new_user.email=extras.email_
    new_user.password=make_password(extras.password_)
    
    if CustomUser.objects.filter(email=new_user.email).exists():
        messages.error(request, 'User with this email already exists.')
        return redirect("login-admin")
    
    if user_type == CustomUser.ADMIN:
        new_user.is_admin=True
        new_user.is_verified=True
        new_user.is_accept_tcs=True
        #new_user.is_superuser=True
        new_user.save()
        messages.success(request, 'Admin account successfully created!')
        return redirect("login-admin")
    

def login_admin_action(request):
    username = request.POST['username']
    password = request.POST['password']
    
    if not(username and password):
        template_name = "accounts/admin/login.html"
        messages.error(request, 'Please provide all the details!!')
        return render(request,template_name=template_name)
    try:
        user = CustomUser.objects.get(username=username) or CustomUser.objects.get(email=username)
        if user.check_password(password):
            request.session['is_admin'] = user.is_admin
            messages.success(request, 'successfully Login!')
            login(request,user)
            return redirect("admin-home")
        else:
            template_name = "accounts/admin/login.html"
            messages.error(request, "Your username and password didn't match.")
            return render(request, template_name )
    except CustomUser.DoesNotExist:
            messages.error(request, 'Invalid Login Credentials!!')
            return redirect("login-admin")

def reset_password_action(request):
    user = CustomUser.objects.get(username=extras.username_)
    if request.method != 'POST':
        raise
    if request.POST.get('password') != request.POST.get('confirm_password'):
        messages.error(request, 'Password and confirm password does not match')
        return redirect('admin-reset-password-view')
    else:
        user.set_password(request.POST.get('password'))
        user.save()
        messages.success(request, 'Password successfully changed!')
        return redirect("login-admin")
    

@login_required(login_url='login-admin') 
def manage_user(request):
    users = CustomUser.objects.all()
    return render (request, 'accounts/admin/users_list.html',{'users':users,
                                                              'users_count':CustomUser.objects.all().count()})

def manage_user_update_view(request,slug):
    user = CustomUser.objects.get(slug=slug)
    context = {'user':user}
    return render (request, 'accounts/admin/users_list_update.html',context)

def manage_user_update(request,slug):
    user = CustomUser.objects.get(slug=slug)
    context = {}
    try:
        user = CustomUser.objects.get(slug=slug)
        context['user'] = user
        if request.method != "POST":
            raise Http404("Bad format.")
        # check is users exists
        elif CustomUser.objects.filter(email=request.POST.get('email')).exists():
                messages.error(request, 'User with this email already exists. Please use different email')
                return render (request, 'accounts/admin/users_list_update.html',context)
        else:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email').lower()
            phone_number = request.POST.get('phone_number')
            
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.phone_number = phone_number
            user.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('admin-manage-user')
    except CustomUser.DoesNotExist:
        # raise Http404("User does not exist.")
        pass
    return render (request, 'accounts/admin/users_list_update.html',context)

@login_required(login_url='login-admin') 
def newsletter_subscriber_view(request):
    
    newsletter_subscribers= NewsletterSubscriber.objects.all()
    return render (request, 'accounts/admin/newsletter_subscriber_list.html',{'newsletter_subscribers':newsletter_subscribers,
                                                                              'newsletter_subscriber_list_count': NewsletterSubscriber.objects.all().count(),
                                                                              })
 
@login_required(login_url='login-admin') 
def delete_newsletter_subscriber(request,slug):
    newsletter_subscriber = NewsletterSubscriber.objects.get(slug=slug)  
    newsletter_subscriber.delete()
    return redirect('newsletter-subscriber-view') 

@login_required(login_url='login-admin') 
def delete_newsletter(request,slug):
    newsletter = Newsletter.objects.get(slug=slug)  
    newsletter.delete()
    return redirect('newsletter-view') 
        
@login_required(login_url='login-admin') 
def delete_user(request,slug):
    user = CustomUser.objects.get(slug=slug)  
    user.delete()
    return redirect('admin-manage-user')

def delete_admin_account(request):
    user = CustomUser.objects.filter(username=extras.username_)
    del request.session['is_admin']
    user.delete()
    logout(request)
    messages.success(request, 'Admin account successfully deleted')
    return redirect('/')

def delete_users_accounts(request):

    user = CustomUser.objects.all()
    newsletter= Newsletter.objects.all()
    newsletter_sub = NewsletterSubscriber.objects.all()
    # payment = Payment.objects.all()
    newsletter.delete()
    newsletter_sub.delete()
    user.delete()
    logout(request)
    messages.success(request, 'All users account successfully deleted')
    return redirect('/')

@login_required(login_url='login-admin')
def logout_admin(request):
    try:
        del request.session['is_admin']
    except KeyError:
        pass
    logout(request)
    messages.success(request, 'Successfully logged out')
    return redirect('login-admin')
    

