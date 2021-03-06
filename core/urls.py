from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'core'

urlpatterns = [
 path("", views.HomeView.as_view() , name="home"),
 path("checkout/", views.checkout , name="checkout"),
 path("product/<slug>/", views.ItemDetailView.as_view() , name="product"),
 path("order-summary/", views.orderSummary, name='order_summary'),
 path("add-to-cart/<slug>/" , views.add_to_cart, name="add_to_cart"),
 path('remove-from-cart/<slug>/', views.remove_from_cart, name='remove_from_cart'),
 path('remove-item-from-cart/<slug>/', views.remove_single_item_from_cart, name='remove_single_item_from_cart'),
 path('payment/<str:payment_option>/', views.payment, name='payment'),
 path('add-coupon/', views.add_coupon , name = 'coupon'),
 path('account/', views.account , name = 'account'),
 path('request-refund', views.RequestRefund , name = 'request_refund'),
 path('order/<str:ref_code>', views.order , name = 'order'),

]



