from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CreateCheckoutSessionView

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('remove-from-cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('orderplaced/', views.order_placed, name='order_placed'),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('payment/', views.payment, name='payment'),
    path('cancel/', views.payment_cancel, name='payment-cancel'),
    path('bill/',views.bill,name='bill'),
    path('invoice_download/',views.invoice_download,name='invoice_download'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('restaurent/', views.restaurent, name='restaurent'),
    path('update_menu/', views.update_menu, name='update_menu'),
    path('manage_orders/', views.manage_orders, name='manage_orders'),
    path('report/', views.report, name='report'),
    path('report_download/<str:date>',views.report_download,name='report_download'),
]
