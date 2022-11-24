import stripe

from django.urls import reverse
from django.views import View
from django.conf import settings
from django.db.models import Sum
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.http import (
    JsonResponse, 
    HttpResponse,
    HttpResponseRedirect,
)

from stripe_payment.models.item import Item
from stripe_payment.models.order import Order


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
        order_id = self.kwargs['pk']
        order = get_object_or_404(Order, pk=order_id)
        context = super(OrderPageView, self).get_context_data(**kwargs)
        context.update({
            'order_id': order_id,
            'cost': order.display_cost,
            'items': order.items.all(),
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
                        'unit_amount': order.cost,
                        'product_data': {
                            'name': 'Total cost',
                        },
                    },
                    'quantity': 1,
                },
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
    ids = request.POST.getlist('item')
    if not ids:
        return HttpResponseRedirect(reverse('cancel-pay'))
    items = Item.objects.filter(id__in=request.POST.getlist('item')).all()
    order = Order.objects.create(
        cost=items.aggregate(Sum('price'))['price__sum'],
    )
    order.items.add(*items)
    return HttpResponseRedirect(reverse('order-page', kwargs={'pk': order.id}))
