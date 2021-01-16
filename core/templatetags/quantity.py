from django import template
from core.models import Order , OrderItem

register = template.Library()

@register.simple_tag
def get_quantity(user , item):
  try:
    order_item = OrderItem.objects.get(user=user , item= item , ordered=False)
  except:
    return 0  
  return order_item.quantity