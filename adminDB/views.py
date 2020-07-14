from django.shortcuts import render, redirect
from django.http import  HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.contrib import messages
from shopping.models import Product, Log, Order, Payment
import json

# Create your views here.

# Index page checks the authention if logined
def index(request):
  if not request.user.is_authenticated:
    return render(request,'login.html')
  return redirect(reverse('mainTable'))

# confirm the correctness of login
@require_POST
def login_view(request):
  username = request.POST['username']
  password = request.POST['password']
  
  user = authenticate(request, username=username, password=password)
  if user is not None:
    login(request, user)
  else:
    messages.warning(request,'Invalid credicant')
  return redirect(reverse('index'))

# logout process
def logout_view(request):
  logout(request)
  messages.info(request,'Logged out successfully!')
  return redirect(reverse('index'))

# Show the order records from DB
@login_required
def mainTable(request):
  orders = Order.objects.all()
  return render(request, 'mainTable.html', {'order': orders})

# Show the order records with given order_id
@login_required
def searchOrder(request):
  if not 'search_id' in request.POST:
    orders = Order.objects.all()
  elif request.POST['search_id'] == '':
    orders = Order.objects.all()
  else:
    orders = Order.objects.all().filter(order_id = request.POST['search_id'])
  return render(request, 'mainTable.html', {'order': orders})

# Show the full log records from DB
@login_required
def FullLog(request):
  logs = Log.objects.all()
  return render(request,'log.html',{'log': logs})

# Show the log recrds with given order_id
@login_required
def searchLog(request):
  if not 'search_id' in request.POST:
    logs = Log.objects.all()

  elif request.POST['search_id'] == '':
    logs = Log.objects.all()
  else:
    order = Order.objects.all().filter(order_id = request.POST['search_id'])
    logs = Log.objects.all().filter(order__in = order)
  return render(request,'log.html',{'log': logs})

# Show the payment information with given order_id
@login_required
def PaymentInfo(request):
  if not 'search_id' in request.POST:
    messages.info(request,'You cannot access payment info')
    return redirect('mainTable')

  elif request.POST['search_id'] == '':
    messages.info(request,'You cannot access payment info')
    return redirect('mainTable')
  order = Order.objects.all().filter(order_id = request.POST['search_id'])
  payments = Payment.objects.filter(order__in = order)
  return render(request,'paymentTable.html',{'payment': payments})

# Show the detail order inforamtion
# Allow emplotee to update the order (providing new order_id)
@login_required
def OrderEdit(request):
  if not 'search_id' in request.POST:
    messages.info(request,'You cannot access Order info')
    return redirect('mainTable')

  elif request.POST['search_id'] == '':
    messages.info(request,'You cannot access Order info')
    return redirect('mainTable')
  order = Order.objects.get(order_id = request.POST['search_id'])
  employee = order.admin

  item_list = json.loads(order.product_list)
  items = []
  
  class Item():
    def __init__(self,id,name,quantity):
      self.id = id
      self.name = name
      self.quantity = quantity


  for element in item_list:
    item = Item(element[0],Product.objects.get(product_id= element[0]).name, element[1])
    items.append(item)
  return render(request,'orderEdit.html',{'items': items, 'employee': order.admin, 'order_id': order.order_id})

# Delete the order manually
@login_required
def delete(request, order_id):
  order = Order.objects.get(order_id = order_id)
  order.admin = request.user.username
  order.status = 'D'
  order.save()

  log = Log()
  log.order = order
  log.action = 'Order delete'
  log.admin = request.user.username
  log.save()

  messages.info(request,'Query Updated')
  return redirect('mainTable')


# Update the order manually (new order_id)
@login_required
def update(request):
  if not 'neworder_id' in request.POST:
    messages.info(request,'You cannot access Update info')
    return redirect('mainTable')

  print(request.POST)
  if request.POST['neworder_id'] == request.POST['order_id']:
    messages.info(request,'new orderID is as same as old orderID')
    return redirect('mainTable')
  try:
    neworder = Order.objects.get(order_id = request.POST['neworder_id'])
    order = Order.objects.get(order_id = request.POST['order_id'])
    order.status = 'D'
    order.admin = request.user.username
    order.save()

    log = Log()
    log.order = order
    log.action = 'Change order'
    log.admin = request.user.username
    log.new_order_id = neworder.order_id
    log.save()
    messages.info(request,'Query Updated')

  except ObjectDoesNotExist as e:
    messages.warning(request, 'new orderID does not exist')
  
  return redirect("mainTable")

