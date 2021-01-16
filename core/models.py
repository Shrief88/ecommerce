from django.db import models
from django.conf import settings
from django.shortcuts import reverse

# Create your models here.

CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sport wear'),
    ('OW', 'Outwear')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

class Item (models.Model):
  title = models.CharField(max_length=100)
  price = models.FloatField()
  discount_price = models.FloatField(blank=True , null=True)
  category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
  label = models.CharField(choices=LABEL_CHOICES, max_length=1)
  slug = models.SlugField()
  description = models.TextField()
  image = models.ImageField(blank = True)
  

  def __str__(self):
    return self.title
  
    

class Order(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  start_data = models.DateTimeField(auto_now_add=True)
  ordered_date = models.DateTimeField()
  ordered = models.BooleanField(default=False)
  billing_address = models.ForeignKey('BillingAddress' , on_delete=models.SET_NULL ,blank=True, null=True)
  payment = models.ForeignKey('Payment' , on_delete=models.SET_NULL ,blank=True, null=True)
  

  def __str__(self):
    return f"order by {self.user.username}"

  def get_total_price(self):
    total = 0
    for item in self.items.all():
      tmp = item.get_final_price()
      total = total + tmp
    return total

  
class OrderItem(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True , null= True)
  order = models.ForeignKey(Order , on_delete=models.CASCADE , related_name='items')
  ordered = models.BooleanField(default=False)
  item = models.ForeignKey(Item, on_delete=models.CASCADE)
  quantity = models.IntegerField(default=1)
  
  
  def __str__(self):
    return f"{self.quantity} of {self.item.title}"

  def get_total_item_price(self):
    return self.quantity * self.item.price  

  def get_total_item_dicount_price(self):
    return self.quantity * self.item.discount_price  

  def get_final_price(self):
    if self.item.discount_price :
      return self.get_total_item_dicount_price()
    else :
      return self.get_total_item_price()   


class BillingAddress(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  name = models.CharField(max_length=100)
  phone = models.CharField(max_length=11)
  secPhone = models.CharField(max_length=11 , blank=True , null= True)
  city = models.CharField(max_length=100)
  address = models.CharField(max_length=100)
  secAdress = models.CharField(max_length=100 , blank=True , null= True)
  

class Payment(models.Model):
  stripe_charge_id = models.CharField(max_length=50)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  amount = models.FloatField()
  timestamp = models.DateTimeField(auto_now_add=True)


