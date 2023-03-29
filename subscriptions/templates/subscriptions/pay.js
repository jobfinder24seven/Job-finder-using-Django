function payWithPayStack(){
    let currency = "NGN";
    let plan = "";
    let ref = "{{ payment.ref }}"
    let obj = {
        key:"{{ paystack_public_key }}",
        email:"{{ payment.payment_by.user_id.email }}",
        amount:"{{ payment.amount_value }}",
        ref:ref,
        callback: function(response){
            window.location.href="{% url 'subscriptions:verify-payment' ref=payment.ref %}";
        }
    }

    if(Boolean(currency)){
        obj.currency = currency.toUpperCase()
    }
    if(Boolean(plan)){
        obj.plan = plan;
    }
    var handler = PaystackPop.setup(obj);
    handler.openIframe();
}
