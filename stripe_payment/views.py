import stripe

from django.views import View
from django.conf import settings
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404

from stripe_payment.models.item import Item


stripe.api_key = settings.STRIPE_SECRET_KEY


class CheckoutSessionCreatingView(View):
    def post(self, request, *args, **kwargs):
        item_id = self.kwargs['pk']
        item = get_object_or_404(Item, pk=item_id)
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': item.price,
                        'product_data': {
                            'name': item.name,
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                'item_id': item.id
            },
            mode='payment',
            success_url=f'{settings.DOMAIN}/success/',
            cancel_url=f'{settings.DOMAIN}/cancel/',
        )
        return JsonResponse({'id': checkout_session.id})


class ItemLandingPageView(TemplateView):
    template_name = 'item.html'

    def get_context_data(self, **kwargs):
        item_id = self.kwargs['pk']
        item = get_object_or_404(Item, pk=item_id)
        context = super(ItemLandingPageView, self).get_context_data(**kwargs)
        context.update({
            'item': item,
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
        })
        return context


class ItemsLandingPageView(TemplateView):
    template_name = 'items.html'

    def get_context_data(self, **kwargs):
        items = Item.objects.all()
        context = super(ItemsLandingPageView, self).get_context_data(**kwargs)
        context.update({
            'items': items,
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
        })
        return context


class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"
