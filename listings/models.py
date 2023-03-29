from django.db import models
from accounts.models import *
from django.urls import reverse
from django.db.models.signals import post_save,pre_save
from django.template.defaultfilters import slugify
from core import extras
from ckeditor.fields import RichTextField
from django.db.models.functions import Now
from datetime import datetime, timedelta
# from django_countries.fields import CountryField
# from ckeditor_uploader.fields import RichTextUploadingField



class Job(models.Model):
    FULL_TIME = 'Full Time'
    PART_TIME = 'Part Time'
    REMOTE = 'Remote'
    INTERSHIP = 'Intership'
    NOT_PROVIDED = 'N/A'
    TIER1 = 'Less than 2yrs'
    TIER2 = '2yrs - 5yrs'
    TIER3 = '5yrs - 10yrs'
    TIER4 = '10yrs - 15yrs'
    TIER5 = 'More than 15yrs'
    
    TYPE_CHOICES = [
        (FULL_TIME, 'Full Time'),
        (PART_TIME, 'Part Time'),
        (REMOTE, 'Remote'),
        (INTERSHIP, 'Intership'),
      
    ]
    
    EXP_CHOICES = [
        (TIER1, 'Less than 2yrs'),
        (TIER2, '2yrs - 5yrs'),
        (TIER3, '5yrs - 10yrs'),
        (TIER4, '10yrs - 15yrs'),
        (TIER5, 'More than 15yrs'),
        (NOT_PROVIDED, 'N/A'),
    ]
    

    
    def logo_dir(instance, filename):
        return 'listings/logo/{1}'.format(instance.company_name, filename)
   

    created_by = models.ForeignKey(Employer, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000, null=True, blank=True)
    description = RichTextField()
    type = models.CharField(max_length=250,choices=TYPE_CHOICES,default=NOT_PROVIDED) 
    min_salary = models.CharField(max_length=100,null=True, blank=True)
    max_salary = models.CharField(max_length=100,null=True, blank=True)
    slug = models.CharField(max_length=5000, null=True, blank=True)
    uniqueId=models.CharField(null=True,blank=True,max_length=50)
    
    company_name = models.CharField(max_length=250)
    company_description  = RichTextField(blank=True, null=True) 
    address=models.CharField(max_length=250)
    location = models.CharField(max_length=100, null=True, blank=True) 
    country = models.CharField(max_length=100, null=True, blank=True)
    #country = CountryField(blank_label='select country')
    email = models.CharField(max_length=500)
    website=models.CharField(max_length=1000, null=True, blank=True)
    qualification = models.CharField(max_length=100,null=True, blank=True)
    experience = models.CharField(max_length=250,choices=EXP_CHOICES,default=NOT_PROVIDED) 
    requirements= RichTextField()
    application_mode=models.CharField(max_length=250,null=True, blank=True)
    logo = models.ImageField(null=True,blank=True,upload_to=logo_dir,default='default.jpg')
    seo_keywords=models.CharField(max_length=2500, null=True, blank=True)
    seo_description=models.CharField(max_length=2500, null=True, blank=True)
    
    direct_list = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    closed_at = models.DateField(null=True, blank=True) # dedeline define by the employer
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # id = models.UUIDField(default=uuid.uuid4, unique=True,
    #                       primary_key=True,
    #                        editable=False)
    objects = models.Manager()
    
    class Meta: 
        ordering = ['-created_at']
        
    def __str__(self):
        return '{} - {}'.format(self.company_name, self.title)
    
    def get_absolute_url(self):
        return reverse('listings:job-detail', kwargs={'slug':self.slug}) 
       

    def save(self,*args,**kwargs):
        if self.uniqueId is None:
            uuid=str(uuid4()).split('-')
            self.uniqueId= uuid[0] # generate uniqueId 
            # self.uniqueId= str(uuid4()).split('-')[0]
            self.slug=slugify(f'{self.title} {uuid}') #company-abc-h2344
            
            
        self.seo_description = f'Apply for {self.title} Job on Job Finder'
        self.seo_keywords = f'{self.title}, Jobs,Trending Job, latest job in {datetime.now().year}'
        super(Job,self).save(*args,**kwargs)
        
# Updating images
@receiver(pre_save, sender=Job)
def pre_save_image(sender, instance, *args, **kwargs):
    """ instance old image file will delete from os """

    try:
        old_img = instance.__class__.objects.get(id=instance.id).logo.path
        try:
            new_img = instance.job.path
        except:
            new_img = None
        if new_img != old_img:
            if os.path.exists(old_img):
                os.remove(old_img)
    except:
        pass

# Applicants:jobseekers      
class Applicant(models.Model):

    NOT_PROVIDED = 'N/A'
    TIER1 = 'Less than 2yrs'
    TIER2 = '2yrs - 5yrs'
    TIER3 = '5yrs - 10yrs'
    TIER4 = '10yrs - 15yrs'
    TIER5 = 'More than 15yrs'
    
    EXP_CHOICES = [
        (TIER1, 'Less than 2yrs'),
        (TIER2, '2yrs - 5yrs'),
        (TIER3, '5yrs - 10yrs'),
        (TIER4, '10yrs - 15yrs'),
        (TIER5, 'More than 15yrs'),
        (NOT_PROVIDED, 'N/A'),
    ]

    def resume_dir(instance, filename):
        return 'listings/applicants/resumes/{0}/{1}'.format(instance.jobseeker_id.user_id.email, filename)
    
    
    job_id = models.ForeignKey(Job, on_delete = models.CASCADE)
    jobseeker_id = models.ForeignKey(JobSeeker, on_delete = models.CASCADE)
    slug = models.CharField(max_length=250, null=True, blank=True)
    
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True) 
    email = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=50, null=True, blank=True)
    address =models.CharField(max_length=250, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    
    qualification = models.CharField(max_length=100,null=True, blank=True)
    experience = models.CharField(max_length=250,choices=EXP_CHOICES,default=NOT_PROVIDED)
    cover_letter = RichTextField()
    portfolio_link=models.URLField(max_length=500)
    resume = models.ImageField(null=True,blank=True,upload_to=resume_dir,default='default.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    
        
    class Meta: 
        ordering = ['-updated_at']
        
    def save(self,*args,**kwargs):
        if self.slug is None:
            uniqueId= str(uuid4()).split('-')[0]
            self.slug=slugify(uniqueId) #JFJ-h2344
        self.slug=slugify(uniqueId) 
        super(Applicant,self).save(*args,**kwargs)
        
class BookmarkJob(models.Model):

    slug = models.CharField(max_length=250, null=True, blank=True)
    bookmarked_by = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)


    def __str__(self):
        return self.job_id.title
    
    def save(self,*args,**kwargs):
        if self.uniqueId is None:
            self.uniqueId= str(uuid4()).split('-')[0]
        super(BookmarkJob,self).save(*args,**kwargs)