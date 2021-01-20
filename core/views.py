from django.contrib import messages
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render , get_object_or_404 , redirect
from django.views.generic import ListView, DetailView
from django.utils import timezone
from .forms import CheckoutForm,CoupounForm,RefundForm
from .models import *
import stripe, random , string

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_ref_code():
  return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))




class HomeView(ListView):
  model = Item
  paginate_by = 8  #number of items that will show in every page
  template_name = "core/home-page.html"


class ItemDetailView(DetailView):
  model = Item 
  template_name = "core/product-page.html"  

  
    
@login_required
def orderSummary(request):
  try:
    order = Order.objects.get(user = request.user , ordered = False)
  except ObjectDoesNotExist :
    messages.error(request,"You do not have an active order")
    return redirect("/") 
  order_items = OrderItem.objects.filter(order=order , ordered= False).all()
  return render(request , 'core/orderSummary.html', {
    'order_items': order_items,
    'order' : order
  }) 
  
@login_required
def add_to_cart(request,slug):
  if request.method == "POST" : 
    quantity = int(request.POST["quantity"])
  else :
    quantity = 1 
  item = get_object_or_404(Item , slug=slug)
  order = Order.objects.filter(user = request.user , ordered = False)
  
  if order.exists():
    order = order[0]
    order_item, created = OrderItem.objects.get_or_create(item=item , user=request.user , order=order , ordered= False)
    if created is True :
      order_item.quantity = quantity
      messages.info(request,"This item was added to your cart.")
    else :
      order_item.quantity += quantity
      messages.info(request,"This item quantity was updated.")
    order_item.save()

  else :
    ordered_date = timezone.now()
    order = Order.objects.create(user=request.user , ordered_date= ordered_date)
    order_item = OrderItem.objects.create(item=item , user=request.user , order=order , ordered=False , quantity=quantity)
    messages.info(request,"This item was added to your cart.")
    
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def remove_single_item_from_cart(request,slug):
  item = get_object_or_404(Item , slug=slug)
  order = Order.objects.filter(user = request.user , ordered = False)
  if order.exists(): 
      order = order[0]    
      order_item = OrderItem.objects.filter(item=item , user=request.user ,  ordered= False , order=order)
      if order_item.exists():
        order_item = order_item[0]
        if order_item.quantity != 1 :
            order_item.quantity -= 1 
            if order_item.quantity == 0:
              order_item.delete()
            order_item.save()
            messages.info(request,"Quantity of this item is reduced.")  
        else :
            order_item.delete()
            messages.info(request,"This item was removed from your cart.")
      else:
          messages.info(request,"This item was not in your cart your cart.")     
  else:
      messages.info(request,"You do not have an active order.")       
  return redirect ("core:order_summary")

@login_required   
def remove_from_cart(request,slug):
  item = get_object_or_404(Item , slug=slug)
  order = Order.objects.filter(user = request.user , ordered = False)
  if order.exists(): 
      order = order[0]    
      order_item = OrderItem.objects.filter(item=item , user=request.user ,  ordered= False , order=order)
      if order_item.exists():
        order_item = order_item[0]
        order_item.delete()
        messages.info(request,"This item was removed from your cart.")
      else:
        messages.info(request,"This item was not in your cart your cart.")     
  else:
      messages.info(request,"You do not have an active order.")       
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

  
@login_required 
def checkout(request):
  try:
    order = Order.objects.get(user = request.user , ordered = False)
  except ObjectDoesNotExist :
    messages.error(request,"You do not have an active order")
    return redirect("/") 
  if request.method == "POST":
    form = CheckoutForm(request.POST)

    if form.is_valid():
      first_name = form.cleaned_data.get('first_name')
      last_name = form.cleaned_data.get('last_name')
      phone = form.cleaned_data.get('phone')
      secPhone = form.cleaned_data.get('secPhone')
      city = form.cleaned_data.get('city')
      address = form.cleaned_data.get('address')
      secAddress = form.cleaned_data.get('secAddress')
      same_shipping_address = form.cleaned_data.get('same_shipping_address')
      same_info = form.cleaned_data.get('same_info') 
      payment_option = form.cleaned_data.get('payment_option')
      
      billing_address = BillingAddress.objects.create(user = request.user,name = first_name+last_name,phone = phone,secPhone = secPhone,city = city,address = address,secAdress = secAddress)
      order.billing_address = billing_address
      order.save()

      if payment_option == 'S':
        return redirect("core:payment" , payment_option = 'stripe')
      elif payment_option == 'P':
        return redirect("core:payment" , payment_option = 'paypal')
      else:
        messages.info(request,"Invalid payment option")
        return redirect("core:checkout",{
          
        })
    
    else:
      messages.info(request,"Failed checked")
      return redirect("core:checkout")

  else :
    order_items = OrderItem.objects.filter(order=order , ordered= False).all()
    return render(request,"core/checkout-page.html",{
      'form' : CheckoutForm(),
      'couponForm' : CoupounForm(),
      'order_items' : order_items,
      'order' : order,
      
    })  

@login_required 
def payment(request,payment_option):
  try:
    order = Order.objects.get(user = request.user , ordered = False)
  except ObjectDoesNotExist :
    return redirect("core:checkout")
    messages.error(request,"You do not have an active order")

  if request.method == "POST":
    token = request.POST.get('stripeToken')
    try:
      # Use Stripe's library to make requests...
      charge = stripe.Charge.create(
      amount=int(order.get_total_price()) * 100, #convert to cents
      currency="usd",
      source=token,  
      )

      payment = Payment.objects.create(
      stripe_charge_id = charge['id'],
      user = request.user,
      amount = order.get_total_price()
      )
      
      order_items = OrderItem.objects.filter(order=order , ordered= False).all()
      for order_item in order_items :
        order_item.ordered = True
        order_item.save()
        
      order.ordered = True
      order.payment = payment
      order.ref_code = create_ref_code()
      order.save()
      
      messages.success(request,'Your order was successful!')
      return redirect('/')

    except stripe.error.CardError as e:
      # Since it's a decline, stripe.error.CardError will be caught
      body = e.json_body
      err = body.get('error', {})
      messages.error(request, f"{err.get('message')}")
      
    except stripe.error.RateLimitError as e:
      # Too many requests made to the API too quickly
      messages.warning(request, "Rate limit error")
      return redirect("core:payment")
    except stripe.error.InvalidRequestError as e:
      # Invalid parameters were supplied to Stripe's API
      messages.warning(request, "Invalid parameters")
      return redirect("core:payment")
    except stripe.error.AuthenticationError as e:
      # Authentication with Stripe's API failed
      # (maybe you changed API keys recently)
      messages.warning(request, "Not authenticated")
      return redirect("core:payment")
    except stripe.error.APIConnectionError as e:
      # Network communication with Stripe failed
      messages.warning(request, "Network error")
      return redirect("core:payment")

    except stripe.error.StripeError as e:
      # Display a very generic error to the user, and maybe send
      # yourself an email
      messages.warning(request, "Something went wrong. You were not charged. Please try again.")
      return redirect("core:payment")
    except Exception as e:
      # Something else happened, completely unrelated to Stripe
      messages.warning(request, "A serious error occurred. We have been notifed.")
      return redirect("core:payment")


  else:
    if order.billing_address :  
      order_items = OrderItem.objects.filter(order=order , ordered= False).all()
      return render(request,'core/payment-page.html', {
        'payment_option': payment_option,
        'order_items' : order_items,
        'order' : order,
        'couponForm' : CoupounForm(),
      })
    else :
      messages.info(request, "You have not added Billing adress")
      return redirect("core:checkout")  



@login_required 
def add_coupon(request):
  if request.method == "POST":
    form = CoupounForm(request.POST)
    if form.is_valid():
      try:
        order = Order.objects.get(user = request.user , ordered = False)
      except ObjectDoesNotExist :
        messages.error(request,"You do not have an active order")
        return redirect("core:checkout")
    
      code = form.cleaned_data.get('code')
      try: 
        coupon = Coupon.objects.get(code=code)  
      except ObjectDoesNotExist :
        messages.error(request,"This coupon does not exist")
        return redirect("core:checkout")

  order.coupon= coupon
  order.save()  
  messages.success(request,"Successfully added coupon")
  return redirect("core:checkout")


def RequestRefund(request):
  if request.method == 'POST' : 
    form = RefundForm(request.POST)
    if form.is_valid() : 
      ref_code = form.cleaned_data.get('ref_code')
      reason = form.cleaned_data.get('reason')
      try : 
        order = Order.objects.get(ref_code = ref_code)
      except ObjectDoesNotExist :
        messages.info(request , 'This order does not exist')
        return redirect('core:request_refund') 

      if order.refund_requested :
        messages.info(request , 'Your request has been sent already')
        return redirect('core:request_refund') 
      order.refund_requested = True
      order.save()
      refund = Refund.objects.create(order = order , reason = reason)
      messages.info(request , 'Your Request has been received')
      return redirect('core:request_refund') 

  else :
    return render(request,'core/request_refund.html', {
      'form' : RefundForm
    })      


