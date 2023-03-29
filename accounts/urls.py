from django.urls import path
from accounts import views,views_employer, views_jobseeker
from subscriptions.views import verify_payment,initiate_payment
from django.views.generic import TemplateView


app_name='accounts'

urlpatterns = [
   
    path('sign-up',TemplateView.as_view(template_name='accounts/signup.html',extra_context={'title': 'Register'}),name="signup"),
    path('sign-in',TemplateView.as_view(template_name='accounts/login.html',extra_context={'title': 'Signin'}),name="login"),
    path('eToken',TemplateView.as_view(template_name='accounts/eToken.html',extra_context={'title': 'eToken'}),name="eToken"),
    path('password-recovery',TemplateView.as_view(template_name='accounts/password_recovery.html',extra_context={'title': 'Password Recovery'}),name="password-recovery"),
    path('jobseeker/sign-up',TemplateView.as_view(template_name='accounts/jobseeker_signup.html',extra_context={'title': 'Jobseeker Account'}),name="jobseeker-signup"),
    path('employer/sign-up',TemplateView.as_view(template_name='accounts/employer_signup.html',extra_context={'title': 'Employer Account'}),name="employer-signup"),
    path('change-password/<int:id>', views.change_password, name='change-password'),

    #Jobseeker
    path('jobseeker/dashboard', views_jobseeker.JobSeekerHomeView.as_view(), name='jobseeker-home'),
    path('jobseeker/manage-jobs', views_jobseeker.manage_job, name='jobseeker-job-manager'),
    path('jobseeker/settings', views_jobseeker.settings, name='jobseeker-settings'),
    path('jobseeker/settings/update', views_jobseeker.update_settings, name='jobseeker-settings-update'),
    path('jobseeker/security', views_jobseeker.security, name='jobseeker-security'),
    path('jobseeker/security/password-update', views_jobseeker.update_password, name='jobseeker-password-update'),
    path('jobseeker/security/username-update', views_jobseeker.update_username, name='jobseeker-username-update'),
    path('jobseeker/notifications', views_jobseeker.notification, name='jobseeker-notification'),
    path('jobseeker/<int:pk>/delete', views_jobseeker.delete_account, name='jobseeker-delete-account'),
    path('jobseeker/delete/', views_jobseeker.delete_account, name='jobseeker-delete-account'),
    path('jobseeker/avater-updated', views_jobseeker.update_avater, name='jobseeker-avater-update'),
    path('jobseeker/avater-removed', views_jobseeker.remove_avater, name='jobseeker-avater-remove'),
    path('jobseeker/resume',views_jobseeker.upload_cv,name='jobseeker-upload-cv'),
    path('jobseeker/resume-update',views_jobseeker.update_cv,name='jobseeker-cv-update'),
    path('jobseeker/feedback',views_jobseeker.jobseeker_feedback,name='jobseeker-feedback'),
    path('jobseeker/feedback/sent',views_jobseeker.jobseeker_feedback_save,name='jobseeker-feedback-action'),
    
    
    #Employer
    path('employer/listing/direct', views_employer.direct_job, name='employer-direct-job'),
    path('employer/listing/featured', views_employer.indirect_job, name='employer-indirect-job'),
    path('employer/applicant/view', views_employer.applicants, name='employer-job-applicants'),
    path('employer/dashboard',views_employer.dashboard, name='employer-home'),
    path('employer/profile',views_employer.settings, name='employer-settings'),
    path('employer/profile/update',views_employer.update_settings, name='employer-settings-update'),
    path('employer/logo/update',views_employer.update_logo, name='employer-logo-update'),
    path('employer/logo/remove',views_employer.remove_logo, name='employer-logo-remove'),
    path('employer/billings', views_employer.billing, name='employer-billing'),
    path('employer/security', views_employer.security, name='employer-security'),
    path('employer/security/password/update', views_employer.update_password, name='employer-password-update'),
    path('employer/security/username/update', views_employer.update_username, name='employer-username-update'),
    path('employer/notifications', views_employer.notification, name='employer-notification'),
    path('employer/feedback',views_employer.employer_feedback,name='employer-feedback'),
    path('employer/feedback/sent',views_employer.employer_feedback_save,name='employer-feedback-action'),
    path('employer/delete', views_employer.delete_account, name='employer-delete-account'),
    path('employer/payment/initiate',initiate_payment, name='employer-initiate-payment'),
    path('<str:ref>/',verify_payment,name="verify-payment"),
    
    
    
    # actions 
    path('sign-up/do', views.signup_action, name='signup-action'),
    path('eToken-validation', views.eToken_action, name='eToken-action'),
    path('eToken/reset', views.reset_eToken_action, name='reset-eToken-action'),
    path('password/reset', views.password_recovery_action, name='password-recovery-action'),
    path('password/change', views.change_password_action, name='change-password-action'),
    path('login/do', views.login_action, name='login-action'),
    path('logout', views.logout_user_action, name='logout'),
    
    
    
    
    
    
]





