from django.shortcuts import render

# Create your views here.
# billing/views.py

import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Customer
from django.http import HttpResponse

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def create_checkout_session(request):
    YOUR_DOMAIN = "http://localhost:5173"  # or your Netlify domain

    try:
        # Create Stripe Customer if not already created
        customer, created = Customer.objects.get_or_create(
            user=request.user,
            defaults={
                "stripe_customer_id": stripe.Customer.create(
                    email=request.user.email
                ).id
            },
        )

        checkout_session = stripe.checkout.Session.create(
            customer=customer.stripe_customer_id,
            payment_method_types=['card'],
            line_items=[{
                'price': 'price_abc123',  # from Stripe dashboard
                'quantity': 1,
            }],
            mode='subscription',
            success_url=YOUR_DOMAIN + '/success',
            cancel_url=YOUR_DOMAIN + '/cancel',
        )

        return JsonResponse({'id': checkout_session.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def stripe_webhook(request):
    return HttpResponse(status=200)
