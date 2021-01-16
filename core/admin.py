from django.contrib import admin
from django.contrib.admin import ModelAdmin, SimpleListFilter


# Register your models here.

from .models import * 


class order_items_inline(admin.TabularInline):
    fields = ['item', 'quantity']
    model = OrderItem 
    extra = 0 


class OrderAdmin(admin.ModelAdmin):
  inlines = (order_items_inline,)

admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order,OrderAdmin)
admin.site.register(BillingAddress)
admin.site.register(Payment)
