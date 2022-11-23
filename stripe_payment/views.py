import json
import stripe

from django.urls import reverse
from django.views import View
from django.conf import settings
from django.core.mail import send_mail
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import (
    JsonResponse, 
    HttpResponse, 
    HttpResponseRedirect,
)


from stripe_payment.models.item import Item
from stripe_payment.models.order import Order


stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"


class OrderLandingPageView(TemplateView):
    template_name = 'order.html'

    def get_context_data(self, **kwargs):
        order_id = self.kwargs['pk']
        order = get_object_or_404(Order, pk=order_id)
        context = super(OrderLandingPageView, self).get_context_data(**kwargs)
        context.update({
            'items': order.items.all(),
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
        })
        return context


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


def create_order(request):
    items = Item.objects.filter(id__in=request.POST.getlist('item')).all()
    order = Order.objects.create()
    order.items.set(items)
    order.save()
    return HttpResponseRedirect(reverse('order-page', kwargs={'pk': order.id}))
