from django import template
from core.models import Order , OrderItem

register = template.Library()

@register.filter
def cart_item_count(user):
   if user.is_authenticated :
      qs = Order.objects.filter(user = user , ordered = False)
      count = 0 
      if qs.exists():  
        for item in OrderItem.objects.filter(order = qs[0]).all() : 
          count += item.quantity
      return count 
      
