from django.contrib import admin
from django.contrib.admin import ModelAdmin, SimpleListFilter


# Register your models here.

from .models import * 


def make_refund_accepted(modeladmin, request , queryset):
  queryset.update(refund_requested= False , refund_granted = True )
make_refund_accepted.short_description = 'Update orders to refund granted'

def make_order_being_delivered(modeladmin, request , queryset):
  queryset.update(being_delivered = True )
make_order_being_delivered.short_description = 'Update orders to being delivered'

def make_order_received(modeladmin, request , queryset):
  queryset.update(being_delivered = True , received = True )
make_order_received.short_description = 'Update orders to received'




class order_items_inline(admin.TabularInline):
    fields = ['item', 'quantity']
    model = OrderItem 
    extra = 0 


class OrderAdmin(admin.ModelAdmin):
  inlines = (order_items_inline,)
  list_display = ['user','ordered','being_delivered','received','refund_requested','refund_granted','coupon','payment','billing_address']
  list_filter = ['user','ordered','being_delivered','received','refund_requested','refund_granted']
  list_display_links = ['user','coupon','payment','billing_address']
  search_fields = ['user__username', 'ref_code']
  actions = [make_refund_accepted , make_order_being_delivered , make_order_received]

class OrderItemAdmin(admin.ModelAdmin):
  list_display = ['item','quantity' , 'user' , 'ordered']  

admin.site.register(Item)
admin.site.register(OrderItem,OrderItemAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(BillingAddress)
admin.site.register(Payment)
admin.site.register(Coupon)


