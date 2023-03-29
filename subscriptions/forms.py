from django import forms
from .models import Payment
from django.views.generic.edit import UpdateView
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment 
        # fields = ('amount','payer')
        fields = ('amount',)
        #exclude = 'user'
        
class PaymentVericationForm(forms.ModelForm):
    class Meta:
        model = Payment 
        fields = ('amount',)
        exclude = ['payment_by']
        

