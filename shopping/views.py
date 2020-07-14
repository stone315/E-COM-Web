from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Product, Payment, Order, Log
from .myclasses import Cart
from mysite.settings import STRIPE_SECRET, STRIPE_PK, DELIVERY_PHONE
from .SMS import SMS
import json
import stripe

# Choice Option for credit card (State)
US_STATE = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]

# Create your views here.

# Index page : Display all items in shop
def index(request):
  products = Product.objects.all().filter(availability=True)
  return render(request,'index.html',{
    'product': products
  })


# Add item to the cart
@require_POST
def add_item(request, product_id):
  cart = Cart(request)
  product = get_object_or_404(Product, product_id = product_id)
  cart.add(product.product_id)
  return redirect("/")

# Review all item in cart before checkout
def review(request):
  cart = Cart(request)
  Q_list = list(range(50))
  return render(request, 'review.html', {'cart':cart, 'list': Q_list, 'totalprice': cart.total_price() })

# Empty the cart (User Action in Review)
@require_POST
def clear_item(request):
  cart = Cart(request)
  cart.clear()
  return redirect("/review")

# Remove ite from the cart (User Action in Review)
@require_POST
def remove_item(request, product_id):
  cart = Cart(request)
  cart.remove(product_id)
  return redirect("/review")

# Change the quantity of item in the cart (User Action in Review)
@require_POST
def change_item(request, product_id, amount):
  cart = Cart(request)
  cart.change(product_id, amount)
  return redirect("/review")

# Payment form for check out
@require_POST
def payment_form(request):

  cart = Cart(request)
  if cart.length() > 0:
    return render(request,'paymentForm.html',{'cart':cart,
      'totalprice': cart.total_price(),
      'count': cart.length(),
      'STATE_list':US_STATE,
      'STRIPE_PK': STRIPE_PK,} )
  else:
    return redirect('/review')

# Check Out process using stripe
@require_POST
def process(request):
  cart = Cart(request)
  stripe.api_key = STRIPE_SECRET
  amount = cart.total_price()*100


  try:
    # using stripe token to send the bill
    token = request.POST.get('stripeToken')
    stripe.Charge.create(
      amount = amount,
      currency = 'usd',
      source=token,
      description="Online shipping order"
    )

    print('Payment succeed')

    # create order record
    order = Order()
    order.receiver_first = request.POST['Shipping_firstName']
    order.receiver_last = request.POST['Shipping_lastName']
    order.receiver_address = request.POST['Shipping_address']
    order.receiver_addresstwo = request.POST['Shipping_address2']
    order.receiver_country = request.POST['Shipping_country']
    order.receiver_state = request.POST['Shipping_state']
    order.receiver_zip = request.POST['Shipping_zip']
    order.product_list = json.dumps(cart.product_list())
    order.status = 'P'
    order.save()
    
    print('Order: Saved in DB')
    # write order to Log
    newlog = Log()
    newlog.order = order
    newlog.action = 'Order confirm'
    newlog.save()

    # create payment
    payment = Payment()
    payment.order = order
    payment.billing_first = request.POST['firstName']
    payment.billing_last = request.POST['lastName']
    payment.billing_address = request.POST['address']
    payment.billing_addresstwo = request.POST['address2']
    payment.billing_country = request.POST['country']
    payment.billing_state = request.POST['state']
    payment.billing_zip = request.POST['zip']
    payment.token_id = request.POST['stripeToken']
    payment.phone = request.POST['phone']
    payment.email = request.POST['email']
    payment.save()

    print('Payment: Saved in DB')
    # write payment to Log
    newlog = Log()
    newlog.order = order
    newlog.action = 'Payment Sucess'
    newlog.save()

    # send message to contact
    sms = SMS(request)
    receiver = '+1' + request.POST['phone']
    sms.message('Payment succeed. Really to ship your order', receiver)


    # send message to delivery department
    sms = SMS(request)
    body = 'Shipping Order:' +'' +'\n Receiver'+ request.POST['Shipping_firstName'] +' '+ request.POST['Shipping_lastName'] + '\n Address: ' + request.POST['Shipping_address'] + ',' + request.POST['Shipping_address2'] + ',' + request.POST['Shipping_country'] + ',' + request.POST['Shipping_state'] + ',' + request.POST['Shipping_zip']
    sms.message(body, DELIVERY_PHONE)


    print('Message: Sent')
    # clear cart
    cart.clear()

    messages.success(request, "Your order was successful!")
    return redirect("/")

  # Handle exceptions
  except stripe.error.CardError as e:
    body = e.json_body
    err = body.get('error', {})
    messages.warning(request, f"{err.get('message')}")
    return redirect("/review")
  except stripe.error.RateLimitError as e:
    # Too many requests made to the API too quickly
    messages.warning(request, "Rate limit error")
    return redirect("/review")
  except stripe.error.InvalidRequestError as e:
    # Invalid parameters were supplied to Stripe's API
    messages.warning(request, "Invalid parameters")
    return redirect("/review")
  except stripe.error.AuthenticationError as e:
    # Authentication with Stripe's API failed
    # (maybe you changed API keys recently)
    messages.warning(request, "Not authenticated")
    return redirect("/review")

  except stripe.error.APIConnectionError as e:
    # Network communication with Stripe failed
    messages.warning(request, "Network error")
    return redirect("/review")
    pass
  except stripe.error.StripeError as e:
    # Display a very generic error to the user, and maybe send
    # yourself an email
    messages.warning(request, "Something went wrong. You were not charged. Please try again.")
    return redirect("/review")
    pass
  except Exception as e:
    messages.warning(request, "A serious error occurred. We have been notifed.")
    return redirect("/review")


  messages.warning(request, "Invalid data received")
  return redirect('review')

