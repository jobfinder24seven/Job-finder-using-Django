from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from accounts import views_admin

urlpatterns = [
    
    
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls',namespace='accounts')),
    path('subscriptions/', include('subscriptions.urls',namespace='subscriptions')),
    path('', include('main.urls',namespace='main')),
    path('', include('listings.urls',namespace='listings')),
    #path('ckeditor/', include('ckeditor_uploader.urls')),
    
    # Employer
    path('jf-admin/employers',views_admin.employer_list,name='admin-employers'),
    path('jf-admin/employers/<slug:slug>/profile', views_admin.employer_profile, name="employer-profile"),
    path('jf-admin/employers/<slug:slug>/payments', views_admin.employer_payments, name="employer-payments"),
    path('jf-admin/employers/<str:ref>/verify-a-payment', views_admin.verify_payment_page, name="verify-payment-page"),
    path('jf-admin/employers/<str:ref>/verified', views_admin.verify_payment, name="verify-payment"),
   
    
    path('jf-admin/manage/listing',views_admin.manage_job, name='admin-manage-listing'),
    path('jf-admin/manage/listing/<slug:slug>/delete',views_admin.delete_job, name='admin-delete-listing'),
    
    # Jobseekr
    path('jf-admin/jobseekers',views_admin.jobseeker_list,name='admin-jobseekers'),
    path('jf-admin/jobseekers/<slug:slug>/profile', views_admin.jobseeker_profile, name="jobseeker-profile"),
    
   
    path('jf-admin/create-newsletter', views_admin.create_newsletter, name='create-newsletter'),
    path('jf-admin/newsletter-view', views_admin.newsletter_view, name='newsletter-view'),
    path('jf-admin/send-newsletter', views_admin.newsletter_action, name='newsletter-action'),
    path('jf-admin/newsletter/<slug:slug>/view', views_admin.newsletter_update_view, name='newsletter-update-view'),
    path('jf-admin/newsletter/<slug:slug>/update',views_admin.newsletter_update_action,name='newsletter-update-action'),
    path('jf-admin/newsletter/<slug:slug>/delete',views_admin.delete_newsletter,name='admin-delete-newsletter'),
    path('jf-admin/newsletter/subscriber-view', views_admin.newsletter_subscriber_view, name='newsletter-subscriber-view'),
    path('jf-admin/newsletter/subscriber/<slug:slug>/delete',views_admin.delete_newsletter_subscriber,name='admin-delete-newsletter-subscriber'),
    
    path('jf-admin/accounts-view',views_admin.manage_user,name='admin-manage-user'),
    path('jf-admin/account/<slug:slug>/view',views_admin.manage_user_update_view,name='admin-manage-user-update-view'),
    path('jf-admin/account/<slug:slug>/update',views_admin.manage_user_update,name='admin-manage-user-update'),
    path('jf-admin/account/<slug:slug>/delete',views_admin.delete_user,name='admin-delete-user'),
    

    # Admin-utilities
    path('jf-admin-create-admin',views_admin.create_admin,name='create-admin'),
    path('jf-admim-reset-password',TemplateView.as_view(template_name = "accounts/admin/reset_password.html",extra_context={'title': 'Jobfinder-Administrator-Reset-Password'}), name='admin-reset-password-view'),
    path('jf-admin-delete-admin-account',views_admin.delete_admin_account,name='delete-admin-account'),
    path('jf-admin-delete-users-accounts',views_admin.delete_users_accounts,name='delete-users-accounts'),
    path('jf-admin-reset-accounts',views_admin.delete_users_accounts,name='delete-users-accounts'),
    path('jf-admin',TemplateView.as_view(template_name = "accounts/admin/login.html",extra_context={'title': 'Jobfinder-Administrator-Login'}), name='login-admin'),
    path('jf-admin/login',views_admin.login_admin_action,name='login-admin-action'),
    path('jf-admin/dashboard',views_admin.AdminHomeView.as_view(), name='admin-home'),
    path('jf-admin/password/changed',views_admin.reset_password_action,name='admin-reset-password-action'),
    path('jf-admin/logout',views_admin.logout_admin,name='logout-admin'),
    path('e-404/',TemplateView.as_view(template_name='404.html',extra_context={'title': 'E404'}),name="404"),

    
  
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'accounts.views.custom_page_not_found_view'
handler500 = 'accounts.views.custom_error_view'
handler403 = 'accounts.views.custom_permission_denied_view'
handler400 = 'accounts.views.custom_bad_request_view'