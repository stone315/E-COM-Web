from django.db import models

# Create your models here.
# Product DB collects all item in shop (including not available items)
class Product(models.Model):
  product_id = models.SmallAutoField(primary_key = True)
  name = models.CharField(max_length = 50)
  discrption = models.CharField(max_length = 200, blank=True, null=True)
  price = models.SmallIntegerField()
  unit = models.CharField(max_length = 20)
  availability = models.BooleanField(default=False)

  def __str__(self):
    print("product ID:", self.product_id)
    print("name: ", self.name)
    print("discrption: ", self.discrption)
    print("price: ", self.price)
    print("unit: ", self.unit)
    return f"\n product ID: {self.product_id} \n name: {self.name} \n discrption: { self.discrption} \n price: {self.price} \n unit: {self.unit}"

# Order DB for recording all order and tracking the status of order
class Order(models.Model):
  order_id = models.AutoField(primary_key = True)
  receiver_first = models.CharField(max_length = 50) 
  receiver_last = models.CharField(max_length = 50)
  receiver_address = models.CharField(max_length = 100)
  receiver_addresstwo = models.CharField(max_length = 100,blank=True, null=True)
  receiver_country = models.CharField(max_length = 20)
  receiver_state = models.CharField(max_length = 20)
  receiver_zip = models.CharField(max_length = 5)
  product_list = models.TextField(null=True) # JSON-serialized (text)
  Time = models.DateTimeField(auto_now=True)

  status_choice = [
    ('P', 'Processing'),
    ('C', 'Completed'),
    ('D', 'Deleted')
  ]
  status = models.CharField(max_length=1,choices=status_choice,default='P')
  admin = models.CharField(max_length=10,blank=True, null=True)


  def __str__(self):
    return f"\n order ID: {self.order_id} \n status: {self.status} \n time:{self.Time}"

# Payment DB for recording payment historical information
class Payment(models.Model):
  order = models.OneToOneField(Order, on_delete=models.CASCADE, primary_key = True)
  billing_first = models.CharField(max_length = 50) 
  billing_last = models.CharField(max_length = 50)
  billing_address = models.CharField(max_length = 100)
  billing_addresstwo = models.CharField(max_length = 100,blank=True, null=True)
  billing_country = models.CharField(max_length = 20)
  billing_state = models.CharField(max_length = 20)
  billing_zip = models.CharField(max_length = 5)
  Time = models.DateTimeField(auto_now_add=True)
  token_id = models.CharField(max_length = 100)
  phone = models.CharField(max_length = 10)
  email = models.EmailField(blank=True, null=True)

  def __str__(self):
    return f"\n order ID: {self.order.order_id} \n token ID: {self.token_id} \n time:{self.Time}"

# Log DB for recording all actions and transcations of order
class Log(models.Model):
  order = models.ForeignKey(Order, on_delete=models.CASCADE)
  action_choices = [
    ('Payment Sucess','Payment Sucess'),
    ('Order confirm','Order confirm'),
    ('Order complete','Order complete'),
    ('Order delete','Order delete'),
    ('Change order','Change order')
  ]
  action = models.CharField(max_length=20, choices=action_choices)
  Time = models.DateTimeField(auto_now_add= True)
  new_order_id = models.IntegerField(blank=True, null=True)
  admin = models.CharField(max_length=10,blank=True, null=True)

  def __str__(self):
    return f"\n  {self.order.order_id}     {self.action}    {self.Time}"
