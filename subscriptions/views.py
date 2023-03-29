from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpRequest, HttpResponse
from accounts.models import *
from listings.models import *
from .models import *
from . import forms
from django.contrib import messages
from django.conf import settings
from django.http import Http404
from django.views.generic.edit import UpdateView


def initiate_payment(request:HttpRequest) -> HttpResponse:
    context  = {}
    user = CustomUser.objects.get(id=request.user.id)
    employer = Employer.objects.get(user_id=user)
    employer_pay=Payment(payment_by=employer,email=user.email)
    if request.method == "POST":
        payment_form = forms.PaymentForm(request.POST,instance=employer_pay)
        context['employer'] = employer
        if payment_form.is_valid():
            payment = payment_form.save()
            context['payment'] = payment
            context['paystack_public_key']= settings.PAYSTACK_PUBLIC_KEY
            return render(request, 'subscriptions/make_payment.html', context)
    else:
        context['payment_form'] = forms.PaymentForm(request.POST,instance=employer)
    return render(request, 'subscriptions/initiate_payment.html',context)
            
        

def verify_payment(request:HttpRequest,ref:str) -> HttpResponse:
    payment = get_object_or_404(Payment,ref=ref)
    verified = payment.verify_payment()
    if verified:
        messages.success(request,'Verification success...')
    else:
        messages.error(request,"verification failed.")
    return redirect('subscriptions:initiate-payment')

def payment_detail(request,ref=None):
    context = {}
    payment = None
    if ref is not None:
        try:
            payment = Payment.objects.get(ref=ref)
            context['payment_by'] = payment.payment_by
        except Payment.DoesNotExist:
            raise Http404
    context['payment'] = payment
    

    template_name = "accounts/payment_detail.html"
    return render(request, template_name, context)


  
            



