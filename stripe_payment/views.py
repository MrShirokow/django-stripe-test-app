import os
import stripe

from django.http import JsonResponse
from django.views import View
from django.conf import settings
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404

from stripe_payment.models.product import Product


stripe.api_key = settings.STRIPE_SECRET_KEY


class CheckoutSessionCreatingView(View):
    def post(self, request, *args, **kwargs):
        product_id = self.kwargs['pk']
        product = get_object_or_404(Product, pk=product_id)
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': product.price,
                        'product_data': {
                            'name': product.name,
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=os.path.join(settings.DOMAIN, '/success/'),
            cancel_url=os.path.join(settings.DOMAIN, '/cancel/'),
        )
        return JsonResponse({'id': checkout_session.id})


class ProductLandingPageView(TemplateView):
    template_name = 'landing.html'

    def get_context_data(self, **kwargs):
        product_id = self.kwargs['pk']
        product = get_object_or_404(Product, pk=product_id)
        context = super(ProductLandingPageView, self).get_context_data(**kwargs)
        context.update({
            'product': product,
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
        })
        return context


class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"
