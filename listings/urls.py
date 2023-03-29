from django.urls import path,include
from listings import views


app_name='listings'

urlpatterns = [
  
    
    path('', views.JobListView.as_view(), name='home'),
    path('create-job',views.create_job_View,name='job-form'),
    path('post-job',views.create_job_action,name='post-job'),
    path('<slug:slug>/', views.job_detail, name="job-detail" ),
    path('<slug:slug>/application/', views.application_form, name="application-form" ),
    path('<slug:slug>/apply/', views.apply, name="apply"),
    path('<slug:slug>/edit/', views.job_form_update_view, name="job-update" ),
    path('<slug:slug>/update/', views.update_job, name="update-job" ),
    path('<slug:slug>/delete/', views.delete_job, name="delete-job" ),
   
    
    path('search-job-location', views.search_job_by_location, name="search-job-location" ),
    path('search-job-location-keyword', views.search_job_by_location_keyword, name="search-job-location-keyword" ),
   
 
 
    path('free-job-postings', views.FreeJobPostPageView.as_view(), name='free-job-post'),
    path('featured-job-posting', views.FeaturedJobPostingPageView.as_view(), name='featured-job-posting'),
    
    
    
    

   
]



