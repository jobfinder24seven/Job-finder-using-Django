from django.shortcuts import render,redirect,reverse
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.decorators import login_required
from . models import *
from django.contrib import messages
from django.contrib.auth.hashers import make_password,check_password
from core import extras
from django.http import Http404

currentYear = datetime.now().year


def users_signup_templates(request,user_type):
    """
    Handle users templating
    """
    if user_type == CustomUser.EMPLOYER:
        template_name = 'accounts/employer_signup.html'
        return render(request, template_name=template_name)
    elif user_type == CustomUser.JOBSEEKER:
        template_name = 'accounts/jobseeker_signup.html'
        return render(request, template_name=template_name)
    else:
        return redirect('')
    
def signup_action(request):
    """
    Provides users to signup
    """
    # employer = 2 | jobseeker=3
    if request.method == 'POST':
        user_type = int(request.POST.get('user_type'))/100
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        email_id = request.POST.get('email_id').lower()
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        terms_and_conditions = request.POST.get('is_accept_tcs')
        
        if not terms_and_conditions:
            tcs  = False
        else:
            tcs = True
        
        if not (user_type and first_name and last_name and phone_number 
                and email_id and password and confirm_password):
            messages.error(request, 'Please provide all the details!!')
            return users_signup_templates(request,user_type)
            
        if password != confirm_password:
            messages.error(request, 'Password and confirm password does not match')
            return users_signup_templates(request,user_type)
        else:
            password = make_password(password)
        
        # check is users exists
        if CustomUser.objects.filter(email=email_id).exists():
                messages.error(request, 'User with this email already exists. Please use different email')
                return users_signup_templates(request,user_type)
        else:
            # create new instance of CustomeUser()
            new_user = CustomUser()
            new_user.username = extras.username() # genarate usernames
            new_user.email = email_id
            new_user.password = password
            new_user.user_type = user_type
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.phone_number = phone_number
            new_user.eToken = extras.eToken() # genarate otp_code
            new_user.terms_and_conditions = tcs
            # new_user.save()
            
            if user_type == CustomUser.EMPLOYER:
                new_user.is_employer=True # optional
                new_user.save()
            elif user_type == CustomUser.JOBSEEKER:
                new_user.is_jobseeker=True # optional
                new_user.save()
            elif user_type == CustomUser.ADMIN:
                new_user.is_admin=True # optional
                new_user.save()
            
            messages.success(request, "Successfully registered")
            # send email
        
            link = request.build_absolute_uri(reverse('accounts:login'))
            template_name='accounts/html_email_templates/activate_account.html'
            subject='Activate your account'
            email_to=new_user.email
            content={'support_team_name':extras.support_team_name,
                     'version':extras.version,
                    'link':link,
                    'eToken':new_user.eToken,
                     'first_name':new_user.first_name,
                     'last_name':new_user.last_name,
                     'email_id':new_user.email}
            msg = f"Enter the OTP code sent to {email_to}"
            extras.send_html_email(request,template_name,content,subject,email_to,msg)
            # return eToken
            return render(request, 'accounts/eToken.html', {'email_id': email_id})


def eToken_action(request):
    
    if request.method == 'GET':
        messages.error(request, 'Bad format!')
        return redirect('404')
    elif request.method == 'POST':
        email_id = request.POST.get('email_id').lower()
        eToken = int(request.POST.get('eToken'))
        
        try:
            user = CustomUser.objects.get(email=email_id)
            if not(eToken):
                messages.error(request, "Provide OTP code")
                return render(request, 'accounts/eToken.html', {'email_id': email_id})
        
            if eToken!=user.eToken:
                user.activate_account = False
                messages.error(request, "Code not match, please enter correct code")
                return render(request, 'accounts/eToken.html', {'email_id': email_id})
            else:
                user.activate_account = True
                user.save()
                messages.success(request, "Your account has been successfully verified")
                return render(request, 'accounts/login.html')    
        except CustomUser.DoesNotExist:
            raise Http404("User does not exist.")
 
        
def reset_eToken_action(request):
    if request.method == 'GET':
        messages.error(request, 'Bad format!')
        return redirect('404')
    elif request.method == 'POST':
        email_id = request.POST.get('email_id').lower()
          
        try:
            user = CustomUser.objects.get(email=email_id)
            user.eToken = extras.eToken()
            user.save()
            
            # send_email
            link = request.build_absolute_uri(reverse('accounts:login'))
            template_name='accounts/html_email_templates/code_request.html'
            subject='Code Request'
            email_to=user.email
            content={'support_team_name':extras.support_team_name,
                     'version':extras.version,
                    'link':link,
                    'eToken':user.eToken,
                     'first_name':user.first_name,
                     'last_name':user.last_name,
                     'email_id':user.email}
            msg = f"Enter the 6-digit code sent to {email_to}"
            extras.send_html_email(request,template_name,content,subject,email_to,msg)
            return render(request, 'accounts/eToken.html', {'email_id': email_id})    
        except CustomUser.DoesNotExist:
            # raise Http404("User does not exist.")
            messages.error(request, 'User does not exist')
            return render(request, 'accounts/signup.html')
        

def password_recovery_action(request):
    if request.method == 'GET':
        messages.error(request, 'Bad format!')
        return redirect('404')
    elif request.method == 'POST':
        email_id = request.POST.get('email_id').lower()
        
        try:
            user=CustomUser.objects.get(email=email_id)
            user.eToken=extras.eToken() # genertae new otp code
            user.save() 
            
            # send_email
            #link = request.build_absolute_uri(reverse('accounts:change-password-action'))
            template_name='accounts/html_email_templates/password_recovery.html'
            subject='Rest your JobFinder Password'
            email_to=user.email
            content={#'link':link,
                    'eToken':user.eToken,
                     'first_name':user.first_name,
                     'last_name':user.last_name,
                     'email_id':user.email}
            msg = f"Enter the OTP code sent to {email_to} to change your passowrd"
            extras.send_html_email(request,template_name,content,subject,email_to,msg)
            return render(request, 'accounts/change_password.html',{'email_id':email_id}) 
        except CustomUser.DoesNotExist:
            #raise Http404("User does not exist.")
            messages.error(request, 'User does not exist')
            template_name = 'accounts/signup.html'
            return render(request, template_name)
        finally:
            pass

def change_password(request,pk):
    try:
        user=CustomUser.objects.get(id=pk)
        return render(request, 'accounts/change_password.html',{'email_id':user.email,'user':user})
    except CustomUser.DoesNotExist:
            # raise Http404("User does not exist.")
            messages.error(request, 'User does not exist')
            template_name = 'accounts/signup.html'
            return render(request, template_name)
        
def change_password_action(request):
    if request.method == 'POST':
        email_id = request.POST.get('email_id').lower()
        eToken = request.POST.get('eToken')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
              
        try:
            user=CustomUser.objects.get(email=email_id)
            if not (email_id and eToken and new_password and confirm_password):
                messages.error(request, 'Please provide all the details!!')
                return render(request, 'accounts/change_password.html',{'email_id':email_id})
        
            if int(eToken)!= user.eToken:
                messages.error(request, 'Code not match!!')
                return render(request, 'accounts/change_password.html',{'email_id':email_id})
            elif new_password != confirm_password:
                messages.error(request, ' Password and confirm password does not match')
                return render(request, 'accounts/change_password.html',{'email':email_id})
            else:
                password = make_password(new_password)
                user.password = password
                user.save()
                messages.success(request,f'Password succefully changed.')
                # sending email to user to inform of the actions

                template_name='accounts/html_email_templates/others.html'
                subject='Password Reset'
                email_to=user.email
                content={'eToken':user.eToken,
                        'first_name':user.first_name,
                        'last_name':user.last_name,
                        'email_id':user.email}
                msg = f"Account password has been changed successfully!"
                extras.send_html_email(request,template_name,content,subject,email_to,msg)

                return render(request, 'accounts/login.html')             
        except CustomUser.DoesNotExist:
            # raise Http404("User does not exist.")
            messages.error(request, 'User does not exist')
            template_name = 'accounts/signup.html'
            return render(request, template_name)
 

def login_action(request):

    if request.method == 'GET':
        messages.error(request, 'Bad format!')
        return redirect('404')
    elif request.method == 'POST':
        email_id = request.POST.get('email_id').lower()
        password = request.POST.get('password')
        
        if not (email_id and password):
            messages.error(request, "Please provide all the details!!")
            template_name = 'accounts/login.html'
            return render(request, template_name) 
        
        try:
            # check if user is exit
            user = CustomUser.objects.get(email=email_id) or CustomUser.objects.get(username=email_id)
            # check if password is coreect
            #password_check = check_password(password, user.password)
            
            if not user.check_password(password):
                messages.error(request, "Your email and password didn't match.")
                return render(request, 'accounts/login.html')
            else:
                # check if user is verify 
                if user.activate_account == False:
                    user.eToken = extras.eToken() # generate new otp code 
                    user.save() # save new generated otp to db
                    # Email otp code to the user email_adress  

                    link = request.build_absolute_uri(reverse('accounts:login'))

                    template_name='accounts/html_email_templates/activate_account.html'
                    subject='Activate your account'
                    email_to=user.email
                    content={'support_team_name':extras.support_team_name,
                            'version':extras.version,
                            'link':link,
                            'eToken':user.eToken,
                            'first_name':user.first_name,
                            'last_name':user.last_name,
                            'email_id':user.email}
                    msg = "Please verify your account"
                    extras.send_html_email(request,template_name,content,subject,email_to,msg)
                    
                    return render(request, 'accounts/eToken.html', {'email_id': user.email})
                else:
                    # Enable session
                    # NB: When session is enabled,
                    # every request (first argument of any view in Django) has a session (dict) attribute.
                    # request.session['dict_attb'] = variable_refrence 
                    
                    request.session['user_id'] = user.id
                    request.session['user_type']  =user.user_type
                    request.session['first_name'] =user.first_name
                    request.session['last_name'] = user.last_name
                    request.session['email_id'] = user.email
                    request.session['username'] = user.username
                    request.session['activate_account'] = user.activate_account
                    request.session['is_employer'] = user.is_employer
                    request.session['is_jobseeker'] = user.is_jobseeker
                    
                  
                    login(request, user)
                    if user.user_type == CustomUser.EMPLOYER:
                        messages.success(request, ' Login Successful')
                        return redirect('accounts:employer-home')
                    
                    elif user.user_type == CustomUser.JOBSEEKER:
                        messages.success(request, ' Login Successful')
                        return redirect('accounts:jobseeker-home')
                    else:
                        user.user_type == CustomUser.ADMIN
                        messages.success(request, ' Login Successful')
                        return redirect('accounts:admin-home')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Invalid Login Credentials!!')
            template_name = 'accounts/login.html'
            return render(request, template_name) 
    # last return: Home page
    return render(request, 'listings/job_list.html')



def logout_user_action(request):
    """
    Provide the ability to logout
    """
    try:
        del request.session['id']
        del request.session['user_type']
        del request.session['first_name']
        del request.session['last_name']
        del request.session['email']
        del request.session['username']
        del request.session['activate_account'] 
        del request.session['is_employer']
        del request.session['is_jobseeker'] 
    except KeyError:
        pass
    logout(request)
    messages.success(request, 'Successfully logged out')
    return redirect('accounts:login')
        
def custom_page_not_found_view(request, exception):
    return render(request, "404.html", {'title':'page_not_found'})

def custom_error_view(request, exception=None):
    return render(request, "500.html", {'title':'server error'})

def custom_permission_denied_view(request, exception=None):
    return render(request, "403.html", {'title':'permission_denied_view'})

def custom_bad_request_view(request, exception=None):
    return render(request, "400.html", {'title':'page_not_found'})
        

            
        
        