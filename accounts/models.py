import os
from uuid import uuid4
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField
from datetime import datetime,date
from django.urls import reverse
from django.core.exceptions import ValidationError


currentYear = datetime.now().year


class CustomUser(AbstractUser):
    ADMIN= 1
    EMPLOYER = 2
    JOBSEEKER = 3
    
    GENDER= (
    ('-', "Gender"),
    ('M', "Male"),
    ('F', "Female"),

)
    
    user_type_data = ((ADMIN, "Admin"),(EMPLOYER, "Employer"),
                      (JOBSEEKER, "Job seeker"))
    
    id = models.AutoField(primary_key=True)
    user_type    = models.PositiveSmallIntegerField(default=1,choices=user_type_data)
    
    is_admin     = models.BooleanField(default=False) # optional
    is_employer  = models.BooleanField(default=False) # optional
    is_jobseeker = models.BooleanField(default=False) # optional
    activate_account  = models.BooleanField(default=False)
    terms_and_conditions= models.BooleanField(default=False) 
    gender = models.CharField(choices=GENDER, max_length=1,default='-')
    phone_number = PhoneNumberField()
    eToken = models.IntegerField(blank=True, null=True)
    slug = models.CharField(max_length=50, null=True, blank=True)
    
    objects = models.Manager()
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
    def save(self,*args,**kwargs):
        if self.slug is None:
            uniqueId= str(uuid4()).split('-')[0]
            self.slug=slugify(f'CU-{uniqueId}-{currentYear}') #company-abc-yyyy
            
        super(CustomUser,self).save(*args,**kwargs)

# Admin_profile
class Admin(models.Model):

    id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
 
# Employer_profile 
class Employer(models.Model):
    DIRECT_EMPLOYER = 'Direct Employer'
    RECRUITMENT_AGENCY = 'Recruitment Agency'
    
    REMOTE = 'Remote'
    INTERSHIP = 'Intership'
    
    NOT_PROVIDED = 'N/A'
    TIER1 = 'Less than 2yrs'
    TIER2 = '2yrs - 5yrs'
    TIER3 = '5yrs - 10yrs'
    TIER4 = '10yrs - 15yrs'
    TIER5 = 'More than 15yrs'
    
    TYPE_CHOICES  = [(NOT_PROVIDED, 'N/A'),
                    (DIRECT_EMPLOYER, 'Direct Employer'),
                    (RECRUITMENT_AGENCY, 'Recruitment Agency')
                    ]
    
    NUMBER_CHOICES= [
        (TIER1, 'Less than 10'),
        (TIER2, '10 - 50'),
        (TIER3, '50 - 100'),
        (TIER4, '100 - 200'),
        (TIER5, 'More than 200'),
        (NOT_PROVIDED, 'N/A'),
    ]

    INDUSTRY_CHOICES = [('N/A', 'select industry type'),('ACCOUNTING', 'Accounting'), ('AIRLINES/AVIATION', 'Airlines/Aviation'), ('ALTERNATIVE DISPUTE RESOLUTION', 'Alternative Dispute Resolution'), ('ALTERNATIVE MEDICINE', 'Alternative Medicine'), ('ANIMATION', 'Animation'),
            ('APPAREL & FASHION', 'Apparel & Fashion'), ('ARCHITECTURE & PLANNING', 'Architecture & Planning'), ('ARTS & CRAFTS', 'Arts & Crafts'), ('AUTOMOTIVE', 'Automotive'), ('AVIATION & AEROSPACE', 'Aviation & Aerospace'),
            ('BANKING', 'Banking'), ('BIOTECHNOLOGY', 'Biotechnology'), ('BROADCAST MEDIA', 'Broadcast Media'), ('BUILDING MATERIALS', 'Building Materials'), ('BUSINESS SUPPLIES & EQUIPMENT', 'Business Supplies & Equipment'), 
            ('CAPITAL MARKETS', 'Capital Markets'), ('CHEMICALS', 'Chemicals'), ('CIVIC & SOCIAL ORGANIZATION', 'Civic & Social Organization'), ('CIVIL ENGINEERING', 'Civil Engineering'), ('COMMERCIAL REAL ESTATE', 'Commercial Real Estate'),
            ('COMPUTER & NETWORK SECURITY', 'Computer & Network Security'), ('COMPUTER GAMES', 'Computer Games'), ('COMPUTER HARDWARE', 'Computer Hardware'), ('COMPUTER NETWORKING', 'Computer Networking'), ('COMPUTER SOFTWARE', 'Computer Software'), 
            ('CONSTRUCTION', 'Construction'), ('CONSUMER ELECTRONICS', 'Consumer Electronics'), ('CONSUMER GOODS', 'Consumer Goods'), ('CONSUMER SERVICES', 'Consumer Services'), ('COSMETICS', 'Cosmetics'), ('DAIRY', 'Dairy'), ('DEFENSE & SPACE', 'Defense & Space'), 
            ('DESIGN', 'Design'), ('EDUCATION MANAGEMENT', 'Education Management'), ('E-LEARNING', 'E-learning'), ('ELECTRICAL & ELECTRONIC MANUFACTURING', 'Electrical & Electronic Manufacturing'), ('ENTERTAINMENT', 'Entertainment'), ('ENVIRONMENTAL SERVICES', 'Environmental Services'),
            ('EVENTS SERVICES', 'Events Services'), ('EXECUTIVE OFFICE', 'Executive Office'), ('FACILITIES SERVICES', 'Facilities Services'), ('FARMING', 'Farming'), ('FINANCIAL SERVICES', 'Financial Services'), ('FINE ART', 'Fine Art'), ('FISHERY', 'Fishery'), ('FOOD & BEVERAGES', 'Food & Beverages'),
            ('FOOD PRODUCTION', 'Food Production'), ('FUNDRAISING', 'Fundraising'), ('FURNITURE', 'Furniture'), ('GAMBLING & CASINOS', 'Gambling & Casinos'), ('GLASS, CERAMICS & CONCRETE', 'Glass, Ceramics & Concrete'), ('GOVERNMENT ADMINISTRATION', 'Government Administration'), ('GOVERNMENT RELATIONS', 'Government Relations'), 
            ('GRAPHIC DESIGN', 'Graphic Design'), ('HEALTH, WELLNESS & FITNESS', 'Health, Wellness & Fitness'), ('HIGHER EDUCATION', 'Higher Education'), ('HOSPITAL & HEALTH CARE', 'Hospital & Health Care'), ('HOSPITALITY', 'Hospitality'), ('HUMAN RESOURCES', 'Human Resources'), ('IMPORT & EXPORT', 'Import & Export'), 
            ('INDIVIDUAL & FAMILY SERVICES', 'Individual & Family Services'), ('INDUSTRIAL AUTOMATION', 'Industrial Automation'), ('INFORMATION SERVICES', 'Information Services'), ('INFORMATION TECHNOLOGY & SERVICES', 'Information Technology & Services'), ('INSURANCE', 'Insurance'), ('INTERNATIONAL AFFAIRS', 'International Affairs'), 
            ('INTERNATIONAL TRADE & DEVELOPMENT', 'International Trade & Development'), ('INTERNET', 'Internet'), ('INVESTMENT BANKING/VENTURE', 'Investment Banking/Venture'), ('INVESTMENT MANAGEMENT', 'Investment Management'), ('JUDICIARY', 'Judiciary'),
            ('LAW ENFORCEMENT', 'Law Enforcement'), ('LAW PRACTICE', 'Law Practice'), ('LEGAL SERVICES', 'Legal Services'), ('LEGISLATIVE OFFICE', 'Legislative Office'), ('LEISURE & TRAVEL', 'Leisure & Travel'), ('LIBRARIES', 'Libraries'), ('LOGISTICS & SUPPLY CHAIN', 'Logistics & Supply Chain'), ('LUXURY GOODS & JEWELRY', 'Luxury Goods & Jewelry'),
            ('MACHINERY', 'Machinery'), ('MANAGEMENT CONSULTING', 'Management Consulting'), ('MARITIME', 'Maritime'), ('MARKETING & ADVERTISING', 'Marketing & Advertising'), ('MARKET RESEARCH', 'Market Research'), ('MECHANICAL OR INDUSTRIAL ENGINEERING', 'Mechanical or Industrial Engineering'), ('MEDIA PRODUCTION', 'Media Production'), ('MEDICAL DEVICE', 'Medical Device'),
            ('MEDICAL PRACTICE', 'Medical Practice'), ('MENTAL HEALTH CARE', 'Mental Health Care'), ('MILITARY', 'Military'), ('MINING & METALS', 'Mining & Metals'), ('MOTION PICTURES & FILM', 'Motion Pictures & Film'), ('MUSEUMS & INSTITUTIONS', 'Museums & Institutions'), ('MUSIC', 'Music'), ('NANOTECHNOLOGY', 'Nanotechnology'), ('NEWSPAPERS', 'Newspapers'), ('NONPROFIT ORGANIZATION MANAGEMENT', 'Nonprofit Organization Management'),
            ('OIL & ENERGY', 'Oil & Energy'), ('ONLINE PUBLISHING', 'Online Publishing'), ('OUTSOURCING/OFFSHORING', 'Outsourcing/Offshoring'), ('PACKAGE/FREIGHT DELIVERY', 'Package/Freight Delivery'), ('PACKAGING & CONTAINERS', 'Packaging & Containers'), ('PAPER & FOREST PRODUCTS', 'Paper & Forest Products'), ('PERFORMING ARTS', 'Performing Arts'), ('PHARMACEUTICALS', 'Pharmaceuticals'), ('PHILANTHROPY', 'Philanthropy'), ('PHOTOGRAPHY', 'Photography'), ('PLASTICS', 'Plastics'), ('POLITICAL ORGANIZATION', 'Political Organization'), ('PRIMARY/SECONDARY', 'Primary/Secondary'),
            ('PRINTING', 'Printing'), ('PROFESSIONAL TRAINING', 'Professional Training'), ('PROGRAM DEVELOPMENT', 'Program Development'), ('PUBLIC POLICY', 'Public Policy'), ('PUBLIC RELATIONS', 'Public Relations'), ('PUBLIC SAFETY', 'Public Safety'), ('PUBLISHING', 'Publishing'), ('RAILROAD MANUFACTURE', 'Railroad Manufacture'), ('RANCHING', 'Ranching'), ('REAL ESTATE', 'Real Estate'), ('RECREATIONAL', 'Recreational'), ('FACILITIES & SERVICES', 'Facilities & Services'), ('RELIGIOUS INSTITUTIONS', 'Religious Institutions'), ('RENEWABLES & ENVIRONMENT', 'Renewables & Environment'), ('RESEARCH', 'Research'), ('RESTAURANTS', 'Restaurants'), ('RETAIL', 'Retail'), ('SECURITY & INVESTIGATIONS', 'Security & Investigations'), ('SEMICONDUCTORS', 'Semiconductors'), ('SHIPBUILDING', 'Shipbuilding'), ('SPORTING GOODS', 'Sporting Goods'), ('SPORTS', 'Sports'), ('STAFFING & RECRUITING', 'Staffing & Recruiting'), ('SUPERMARKETS', 'Supermarkets'), ('TELECOMMUNICATIONS', 'Telecommunications'), ('TEXTILES', 'Textiles'), ('THINK TANKS', 'Think Tanks'), ('TOBACCO', 'Tobacco'), ('TRANSLATION & LOCALIZATION', 'Translation & Localization'), ('TRANSPORTATION/TRUCKING/RAILROAD', 'Transportation/Trucking/Railroad'), ('UTILITIES', 'Utilities'), ('VENTURE CAPITAL', 'Venture Capital'), ('VETERINARY', 'Veterinary'), ('WAREHOUSING', 'Warehousing'), ('WHOLESALE', 'Wholesale'), ('WINE & SPIRITS', 'Wine & Spirits'),
            ('WIRELESS', 'Wireless'), ('WRITING & EDITING', 'Writing & Editing')]
    
    
    def logo_dir(instance, filename):
        return 'accounts/employers/logo/{0}-{1}'.format(instance.user_id.email, filename)
    
  
    # id = models.UUIDField(default=uuid4, unique=True,
    #                       primary_key=True,
    #                       editable=False)
    id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    slug = models.CharField(max_length=50, null=True, blank=True)
    company_name = models.CharField(max_length=500, null=True, blank=True)
    company_industry = models.CharField(max_length=250,choices=INDUSTRY_CHOICES,default=NOT_PROVIDED)
    company_type = models.CharField(max_length=250,choices=TYPE_CHOICES,default=NOT_PROVIDED)
    company_description = RichTextField()
    address = models.CharField(max_length=250, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    number_of_employees = models.CharField(max_length=250,choices=NUMBER_CHOICES,default=1)
    website= models.CharField(max_length=500, null=True, blank=True)
    logo = models.FileField(null=True,blank=True,
                              upload_to=logo_dir,default='default.png')
    
    payment_verified = models.BooleanField(default=False)  
    next_payment_date = models.CharField(max_length=50,null=True, blank=True)
    
    subscribed_to_newsletter = models.BooleanField(default=False)
    security_alert = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = models.Manager()
    
    def get_absolute_url(self):
        return reverse('employer-profile', kwargs={'slug':self.slug}) 
    
    def save(self,*args,**kwargs):
        if self.slug is None:
            uniqueId= str(uuid4()).split('-')[0]
            self.slug=slugify(f'ER-{uniqueId}-{currentYear}') #company-abc-yyyy
            
        super(Employer,self).save(*args,**kwargs)
        

# Jobseeker_profile
class JobSeeker(models.Model):
    
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
        (NOT_PROVIDED, 'N/A'),
    ]
    
    EXP_CHOICES = [
        (TIER1, 'Less than 2yrs'),
        (TIER2, '2yrs - 5yrs'),
        (TIER3, '5yrs - 10yrs'),
        (TIER4, '10yrs - 15yrs'),
        (TIER5, 'More than 15yrs'),
        (NOT_PROVIDED, 'N/A'),
    ]
    

    def avater_dir(instance, filename):
        return 'accounts/jobseekers/avater/{0}/{1}'.format(instance.user_id.email, filename)
    
    def resume_dir(instance, filename):
        return 'accounts/jobseekers/resumes/{0}/{1}'.format(instance.user_id.email, filename)
        
    id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    slug = models.CharField(max_length=5000, null=True, blank=True)
    
    dob =  models.DateField(null=True, blank=True)
    address =models.CharField(max_length=250, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    summary = RichTextField() # job description
    experience=models.CharField(max_length=250,choices=EXP_CHOICES,default=NOT_PROVIDED) 
    education=models.CharField(max_length=50, null=True, blank=True) # qualification
    skills=RichTextField()
    portfolio_link=models.CharField(max_length=1000, null=True, blank=True)
    resume = models.FileField(null=True,blank=True,
                              upload_to=resume_dir,default='default.png')
    avater = models.FileField(null=True,blank=True,
                              upload_to=avater_dir,default='default.png')
    display_resume =models.BooleanField(default=False) 
    min_salary = models.BigIntegerField()
    max_salary = models.BigIntegerField()
    job_type= models.CharField(max_length=250,choices=TYPE_CHOICES,default=NOT_PROVIDED)
 
    subscribed_to_newsletter = models.BooleanField(default=False)
    security_alert = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    
    def save(self,*args,**kwargs):
        if self.slug is None:
            uniqueId= str(uuid4()).split('-')[0]
            self.slug=slugify(f'JS-{uniqueId}-{currentYear}') #company-code-year
  
        super(JobSeeker,self).save(*args,**kwargs)
                 

class FeedBackEmployer(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.CharField(max_length=50, null=True, blank=True)
    employer_id = models.ForeignKey(Employer, on_delete=models.CASCADE)
    
    feedback = RichTextField()
    feedback_reply = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    
    def save(self,*args,**kwargs):
        if self.slug is None:
            uniqueId= str(uuid4()).split('-')[0]
            self.slug=slugify(f'FBER-{uniqueId}-{currentYear}') #company-abc-h2344
       
        super(FeedBackEmployer,self).save(*args,**kwargs)
 
 
class FeedBackJobSeeker(models.Model):
    id = models.AutoField(primary_key=True)
    uniqueId=models.CharField(null=True,blank=True,max_length=500)
    slug = models.CharField(max_length=50, null=True, blank=True)
    
    jobseeker_id = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)
    feedback = RichTextField()
    feedback_reply = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    
    def save(self,*args,**kwargs):
        if self.slug is None:
            uniqueId= str(uuid4()).split('-')[0]
            self.slug=slugify(f'FBJS-{uniqueId}-{currentYear}') #company-abc-h2344
    
        super(FeedBackJobSeeker,self).save(*args,**kwargs)
 

@receiver(post_save, sender=Employer)
def create_employer_feedback(sender, instance, created,  **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
        FeedBackEmployer.objects.create(employer_id=instance,
                                        feedback = '',
                                        feedback_reply = '',
                                                ) 

@receiver(post_save, sender=JobSeeker)
# signal_for_notification
def create_jobseeker_feedback(sender, instance, created,  **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
        FeedBackJobSeeker.objects.create(jobseeker_id=instance,
                                        feedback = '',
                                        feedback_reply = '',
                                                )
    
# Signals for custome_user
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created,  **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
        if instance.user_type == 1:
            Admin.objects.create(user_id=instance)
            
        if instance.user_type == 2:
            Employer.objects.create(user_id=instance,
                                    company_name="",
                                    company_industry="",
                                    company_type="",
                                    address="",
                                    location="",
                                    country="",
                                    number_of_employees="",
                                    website="",
                                    company_description="",
                                    payment_verified=0,
                                    logo="",
                                    subscribed_to_newsletter=0,
                                    security_alert=1,
                                    
                                   )
            
        if instance.user_type == 3:
            JobSeeker.objects.create(user_id=instance,
                                    #dob="",
                                    address="",
                                    location="",
                                    country="",
                                    summary="",
                                    experience="",
                                    education="",
                                    skills="",
                                    portfolio_link="",
                                    resume="",
                                    avater="",
                                    display_resume=0,
                                    min_salary=0,
                                    max_salary=0,
                                    job_type="",
                                    subscribed_to_newsletter=0,
                                    security_alert=1,
                                    
                                    )

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.employer.save()
    if instance.user_type == 3:
        instance.jobseeker.save()
        
        

# Updating images  
# @receiver(pre_save, sender=Employer)
# def pre_save_image(sender, instance, *args, **kwargs):
#     """ instance old image file will delete from os """
#     max_upload_limit = 5*1024*1024   # 5mb
#     try:
#         old_img = instance.__class__.objects.get(id=instance.id).logo.path
#         try:
#             new_img = instance.employer.path
#         except:
#             new_img = None
#         if new_img != old_img:
#             if os.path.exists(old_img):
#                 os.remove(old_img)
#     except:
#         pass
    
# @receiver(pre_save, sender=JobSeeker)
# def pre_save_image(sender, instance, *args, **kwargs):
#     """ instance old image file will delete from os """
#     try:
#         old_img = instance.__class__.objects.get(id=instance.id).avater.path
#         try:
#             new_img = instance.jobseeker.path
#         except:
#             new_img = None
#         if new_img != old_img:
#             if os.path.exists(old_img):
#                 os.remove(old_img)
#     except:
#         pass
    
#     try:
#         old_resume = instance.__class__.objects.get(id=instance.id).resume.path
#         try:
#             new_resume = instance.jobseeker.path
#         except:
#             new_resume = None
#         if new_resume != old_resume:
#             if os.path.exists(old_resume):
#                 os.remove(old_resume)
#     except:
#         pass
        
        
    