from django.urls import path, re_path

from stripe_payment.views import (
    CheckoutSessionCreatingView,
    ProductLandingPageView,
    ProductsLandingPageView,
    CancelView,
    SuccessView,
)


urlpatterns = [
    path('', ProductsLandingPageView.as_view(), name='products-page'),
    re_path(r'^buy/(?P<pk>[0-9]*)/?$', CheckoutSessionCreatingView.as_view(), name='buy-item'),
    re_path(r'^item/(?P<pk>[0-9]*)/?$', ProductLandingPageView.as_view(), name='item-page'),
    re_path(r'^success/?$', SuccessView.as_view(), name='success-pay'),
    re_path(r'^cancel/?$', CancelView.as_view(), name='cancel-pay')
]
