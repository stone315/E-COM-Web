# Django Ecommerical Web Server

## Discription
This project builds a e-commerical Web Server which provides User Interface for custemer to explore/buy the products and manager to manage the orders.

---
Custemer "Can"
1. Look up the products
2. Modifiy the items in cart on summary Package
3. Pay the bill using cards (service provided by stripe API)

---
Manager "Can"
1. Look up the order and order's payment history
2. Read the full Log of order's action (change)
3. Edit/Cancel the order

## Flow Diagram (Has been modify that is different to the final code)
![Flow Chart](https://github.com/stone315/E-COM-Web/blob/master/Django1.jpg)



## Require Package


* Django = "3.0"

~~~
pip install django
~~~

* python = "3.8"
* stripe = "2.48.0"

~~~
pip install stripe
~~~

* twilio = "6.44.0"

~~~
pip install twilio
~~~

*Sqlite3


## DataBase (DB)
### Tables
(For detail, go through shopping/models.py)

#### Product's Fields

* product_id
* name 
* discrption(optional)
* price
* unit
* availability(Bollean)

#### Log's Fields

* order
* action 
* Time
* new_order_id
* admin (optional)

#### Order's Fields

* order_id
* receiver_first
* receiver_last
* receiver_address
* receiver_addresstwo (optional)
* receiver_country
* receiver_state
* receiver_zip
* product_list
* Time
* status
* Admin (optional)


#### Payment's Fields

* order
* billing_first
* billing_last
* billing_address
* billing_addresstwo (optional)
* billing_country 
* billing_state
* billing_zip
* Time 
* token_id
* phone
* email


## Run the server

1. Setup

_go to mysite.setting_

_Add STRIPE KEYS which are the public and secret key in your stripe account_
  
  STRIPE_PK = 'xxxxx'
  STRIPE_SECRET = 'xxxxxx'


_Add Twillo KEYS which are the account SID and account token in your twilio account_

 ACCOUNT_SID = 'xxx'
 AUTH_TOKEN = 'xxx'

_Add phone number: The phone sender is the number whicn is used to send messages and delivery phone is the number that will recivce the message and make delivery_

** make sure the phone sender is linked in your twilio account**
PHONE_SENDER = '+1xxxxxxxxxx'
DELIVERY_PHONE = '+1xxxxxxxxxx'


2. DB setting

_Setup Admin account for your DB_

In shell, type

~~~
python manage.py createsuperusers
~~~

Registe with UserID, Password and Email Address

3. Run the server

~~~
python manage.py runserver 0.0.0.0:3000
~~~
