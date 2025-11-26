from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('create-payment-intent/<int:order_id>/', views.create_payment_intent, name='create_payment_intent'),
    path('payment/<int:order_id>/', views.payment_page, name='payment_page'),
    path('payment-success/<int:order_id>/', views.payment_success, name='payment_success'),
    path('payment-cancelled/<int:order_id>/', views.payment_cancelled, name='payment_cancelled'),
    path('stripe-webhook/', views.stripe_webhook, name='stripe_webhook'),
]

