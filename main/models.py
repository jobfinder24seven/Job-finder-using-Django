from django.db import models
from uuid import uuid4
from datetime import datetime
from django.template.defaultfilters import slugify

currentYear = datetime.now().year

class NewsletterSubscriber(models.Model):
    email = models.EmailField()
    slug = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.email
    
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
    def save(self,*args,**kwargs):
        if self.slug is None:
            uniqueId= str(uuid4()).split('-')[0]
            self.slug=slugify(f'NLS-{uniqueId}-{currentYear}') # company-abc-yyyy
            
        super(NewsletterSubscriber,self).save(*args,**kwargs)

class Newsletter(models.Model):
    EMAIL_STATUS_CHOICES=(
        ('Draft', 'Draft'),
        ('Published', 'Published'),
    )
    
    slug = models.CharField(max_length=50, null=True, blank=True)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    # email_to=models.ManyToManyField(NewsletterSubscriber)
    email_to= models.IntegerField(blank=True, null=True)
    status=models.CharField(max_length=10,choices=EMAIL_STATUS_CHOICES)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.subject
    
    def save(self,*args,**kwargs):
        if self.slug is None:
            uniqueId= str(uuid4()).split('-')[0]
            self.slug=slugify(f'NL-{uniqueId}-{currentYear}') # company-abc-yyyy
            
        super(Newsletter,self).save(*args,**kwargs)