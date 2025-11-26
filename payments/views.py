import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from decimal import Decimal

from orders.models import Order
from .models import Payment

# Set Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def create_payment_intent(request, order_id):
    """Create a Stripe PaymentIntent for the order"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Convert amount to cents (Stripe uses cents)
    amount_in_cents = int(order.order_total * 100)
    
    try:
        # Create PaymentIntent
        intent = stripe.PaymentIntent.create(
            amount=amount_in_cents,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                'order_id': order.id,
                'user_id': request.user.id,
            }
        )
        
        # Create or update Payment record
        payment, created = Payment.objects.get_or_create(
            order=order,
            defaults={
                'stripe_payment_intent_id': intent.id,
                'stripe_client_secret': intent.client_secret,
                'amount': order.order_total,
                'currency': settings.STRIPE_CURRENCY,
                'status': 'pending'
            }
        )
        
        if not created:
            payment.stripe_payment_intent_id = intent.id
            payment.stripe_client_secret = intent.client_secret
            payment.amount = order.order_total
            payment.status = 'pending'
            payment.save()
        
        return JsonResponse({
            'client_secret': intent.client_secret,
            'publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
        })
        
    except stripe.error.StripeError as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def payment_page(request, order_id):
    """Display the payment page with Stripe Elements"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Check if payment already exists
    try:
        payment = Payment.objects.get(order=order)
        if payment.status == 'completed':
            messages.success(request, 'Payment already completed!')
            return redirect('order_complete', order_id=order.id)
    except Payment.DoesNotExist:
        pass
    
    context = {
        'order': order,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, 'payments/payment.html', context)

@login_required
def payment_success(request, order_id):
    """Handle successful payment"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    try:
        payment = Payment.objects.get(order=order)
        payment.status = 'completed'
        payment.save()
        
        # Update order status
        order.status = 'Completed'
        order.save()
        
        messages.success(request, 'Payment completed successfully!')
        return redirect('order_complete', order_id=order.id)
        
    except Payment.DoesNotExist:
        messages.error(request, 'Payment not found!')
        return redirect('place_order')

@login_required
def payment_cancelled(request, order_id):
    """Handle cancelled payment"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    try:
        payment = Payment.objects.get(order=order)
        payment.status = 'cancelled'
        payment.save()
        
        messages.info(request, 'Payment was cancelled.')
        return redirect('place_order')
        
    except Payment.DoesNotExist:
        messages.error(request, 'Payment not found!')
        return redirect('place_order')

@csrf_exempt
@require_POST
def stripe_webhook(request):
    """Handle Stripe webhooks"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)
    
    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        handle_successful_payment(payment_intent)
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        handle_failed_payment(payment_intent)
    
    return HttpResponse(status=200)

def handle_successful_payment(payment_intent):
    """Handle successful payment from webhook"""
    try:
        payment = Payment.objects.get(
            stripe_payment_intent_id=payment_intent['id']
        )
        payment.status = 'completed'
        payment.save()
        
        # Update order status
        order = payment.order
        order.status = 'Completed'
        order.save()
        
    except Payment.DoesNotExist:
        pass

def handle_failed_payment(payment_intent):
    """Handle failed payment from webhook"""
    try:
        payment = Payment.objects.get(
            stripe_payment_intent_id=payment_intent['id']
        )
        payment.status = 'failed'
        payment.save()
        
    except Payment.DoesNotExist:
        pass