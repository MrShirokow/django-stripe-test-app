import stripe

from itertools import islice
from django.urls import reverse
from django.views import View
from django.conf import settings
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.http import (
    JsonResponse, 
    HttpResponse,
    HttpResponseRedirect,
)

from stripe_payment.models.item import Item
from stripe_payment.models.order import Order
from stripe_payment.models.order_item import OrderItem


stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessView(TemplateView):
    '''
    View for success page after payment
    '''
    template_name = "success.html"


class CancelView(TemplateView):
    '''
    View for cancel page after payment
    '''
    template_name = "cancel.html"


class OrderPageView(TemplateView):
    '''
    View for page with order items
    '''
    template_name = 'order.html'

    def get_context_data(self, **kwargs) -> dict:
        order_id = self.kwargs.get('pk')
        order = get_object_or_404(Order, pk=order_id)
        context = super(OrderPageView, self).get_context_data(**kwargs)
        context.update({
            'order_id': order_id,
            'cost': order.display_cost,
            'order_items': order.order_items.all(),
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
        })
        return context


class HomePageView(TemplateView):
    '''
    View for main page with product items
    '''
    template_name = 'home.html'

    def get_context_data(self, **kwargs) -> dict:
        items = Item.objects.all()
        context = super(HomePageView, self).get_context_data(**kwargs)
        context.update({
            'items': items,
        })
        return context


class ItemPageView(TemplateView):
    '''
    View for item page
    '''
    template_name = 'item.html'

    def get_context_data(self, **kwargs) -> dict:
        item_id = self.kwargs.get('pk')
        item = get_object_or_404(Item, pk=item_id)
        context = super(ItemPageView, self).get_context_data(**kwargs)
        context.update({
            'item': item,
        })
        return context


class CheckoutSessionCreatingView(View):
    '''
    View to create a session for order payment
    '''
    def post(self, request, *args, **kwargs) -> JsonResponse:
        order_id = self.kwargs['pk']
        order = get_object_or_404(Order, pk=order_id)
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': order_item['item__price'],
                        'product_data': {
                            'name': order_item['item__name'],
                        },
                    },
                    'quantity': order_item['quantity'],
                } 
                for order_item in order.order_items.values(
                    'quantity', 
                    'item__price', 
                    'item__name',
                )
            ],
            metadata={
                'order_id': order.id,
            },
            mode='payment',
            success_url=f'{settings.DOMAIN}/success/',
            cancel_url=f'{settings.DOMAIN}/cancel/',
        )
        return JsonResponse({'id': checkout_session.id})


def create_order(request) -> HttpResponse:
    '''
    View for create order and order items. After creating, redirect to order page 
    '''
    items = request.POST.getlist('item')
    quantities = request.POST.getlist('quantity')
    if not items:
        return HttpResponseRedirect(reverse('cancel-pay'))
    creation_data = list(zip(items, quantities))
    order = Order.objects.create()
    batch_size = 100
    item_iterator = (
        OrderItem(
            order_id=order.id,
            item_id=item_id,
            quantity=quantity,
        ) 
        for item_id, quantity in creation_data
    )
    while True:
        batch = list(islice(item_iterator, batch_size))
        if not batch:
            break
        OrderItem.objects.bulk_create(batch, batch_size)
    return HttpResponseRedirect(reverse('order-page', kwargs={'pk': order.id}))
