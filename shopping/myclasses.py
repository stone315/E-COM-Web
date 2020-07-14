from .models import Product


CART_SESSION_ID = 'Cart'

# Class Cart represent the items and behaviors in cart
class Cart():

  def __init__(self, request):
    # check session if user has the session record
    self.session = request.session
    cart = self.session.get(CART_SESSION_ID)

    if not cart:
      self.session[CART_SESSION_ID] = {}
      cart = self.session[CART_SESSION_ID]
    self.cart = cart
  
  # Add new Item
  def add(self, ID):
    ID = str(ID)
    if  ID not in self.cart.keys():
      self.cart[ID] = {'quantity': 1,'price': Product.objects.get(product_id=ID).price}
    else:
      self.cart[ID]['quantity'] += 1
    self.save() 

  # Change the quantiy of item "ID"
  def change(self, ID, amount):
    ID = str(ID)
    if amount == 0:
      self.remove(ID)
    else:
      self.cart[ID]['quantity'] = amount
      self.cart[ID]['price'] = Product.objects.get(product_id=ID).price
    self.save()
  
  # Remove item from the cart
  def remove(self, ID):
    ID = str(ID)
    if ID in self.cart:
      del self.cart[ID]
      self.save()

  # Clear all item
  def clear(self):
    self.cart = {}
    self.save()

  # Save the cart information in Session
  def save(self):
    self.session[CART_SESSION_ID] = self.cart
    self.session.modified = True

  # loop the item in the cart
  # use this to retrive all items for checkout
  def __iter__(self):

    product_ids = [ int(i) for i in self.cart.keys()]
    products = Product.objects.filter(product_id__in = product_ids)

    for item in products:
      self.cart[str(item.product_id)]['id'] = item.product_id
      self.cart[str(item.product_id)]['name'] = item.name 
      self.cart[str(item.product_id)]['unit'] = item.unit 
      self.cart[str(item.product_id)]['total'] = item.price * self.cart[str(item.product_id)]['quantity']
    
    for item in self.cart.values():
      yield item 

  # get the total price
  def total_price(self):
    total = 0
    for item in self.cart.values():
      total += item['quantity']*item['price']
    
    return total

  # count the number of items in the cart
  def length(self):
    length = 0
    for item in self.cart.values():
      length = length + 1
    return length

  # provide the list of item as record of order
  def product_list(self):
    ls = []
    for ID in self.cart.keys():
      ls.append([ID, self.cart[ID]['quantity']])
    return ls

