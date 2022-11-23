from django.urls import path, re_path

from stripe_payment.views import (
    CheckoutSessionCreatingView,
    ItemLandingPageView,
    ItemsLandingPageView,
    CancelView,
    SuccessView,
)


urlpatterns = [
    path('', ItemsLandingPageView.as_view(), name='items-page'),
    re_path(r'^buy/(?P<pk>[0-9]*)/?$', CheckoutSessionCreatingView.as_view(), name='buy-item'),
    re_path(r'^item/(?P<pk>[0-9]*)/?$', ItemLandingPageView.as_view(), name='item-page'),
    re_path(r'^success/?$', SuccessView.as_view(), name='success-pay'),
    re_path(r'^cancel/?$', CancelView.as_view(), name='cancel-pay')
]
