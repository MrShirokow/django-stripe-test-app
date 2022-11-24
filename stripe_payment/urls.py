from django.urls import path, re_path

from stripe_payment.views import (
    CheckoutSessionCreatingView,
    OrderPageView,
    # ItemLandingPageView,
    HomePageView,
    CancelView,
    SuccessView,
    create_order,
)


urlpatterns = [
    path('', HomePageView.as_view(), name='home-page'),
    re_path(r'^order/create/?$', create_order, name='create-order'),
    re_path(r'^order/(?P<pk>[0-9]*)/?$', OrderPageView.as_view(), name='order-page'),
    re_path(r'^order/(?P<pk>[0-9]*)/buy/?$', CheckoutSessionCreatingView.as_view(), name='buy-items'),
    # re_path(r'^item/(?P<pk>[0-9]*)/?$', ItemLandingPageView.as_view(), name='item-page'),
    re_path(r'^success/?$', SuccessView.as_view(), name='success-pay'),
    re_path(r'^cancel/?$', CancelView.as_view(), name='cancel-pay'),
]
