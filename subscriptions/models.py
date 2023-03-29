import secrets
from django.db import models
from accounts.models import Employer
from django.urls import reverse
from .paystack import PayStack


# User Payment Model
class Payment(models.Model):
    AMOUNT_CHOICES = (
    (0.00, "select amount"),
    (5000.00, "#5, 000"),
    (10000.00, "#10, 000"),
    (20000.00, "Pay #20,000 get #30,000"),
    (30000.00, "Pay #30,000 get #45, 000"),
    (50000.00, "Pay #50, 000 get #75, 000"),
    )
    payment_by = models.ForeignKey(Employer, on_delete=models.CASCADE,default=None)
    #amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    amount= models.DecimalField(
        max_digits=10,
        decimal_places=2,
        choices = AMOUNT_CHOICES,
        default=0.00
        )
    ref=models.CharField(max_length=100)
    email = models.EmailField()
    verified = models.BooleanField(default=False) 
    created_date = models.DateTimeField(auto_now_add=True)
    next_payment_date= models.CharField(max_length=50, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
   
    class Meta:
        ordering = ('created_date',)

    def __str__(self):
        return f'Payment: {self.amount} by {self.payment_by.company_name}'
    
    def get_absolute_url(self):
        return reverse('subscriptions:verify-payment', kwargs={'ref':self.ref}) 
    
    def save(self,*args,**kwargs) -> None:
        while not self.ref:
            ref = secrets.token_urlsafe(18) # secreat is used to generate API keys
            objects_with_similar_ref = Payment.objects.filter(ref=ref)
            if not objects_with_similar_ref:
                self.ref = ref
                
            
                
            super().save(*args, **kwargs)
             
    def amount_value(self) -> int:
        return self.amount * 100
        
    def verify_payment(self):
        paystack = PayStack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            if result['amount']/100 == self.amount:
                self.verified = True
            self.save()
        if self.verified:
            return True
        #return False
  

        

   