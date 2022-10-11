from django.urls import re_path

from stripe_payment.views import (
    CheckoutSessionCreatingView,
    ProductLandingPageView,
    CancelView,
    SuccessView,
)


urlpatterns = [
    re_path(r'^create-checkout-session/(?P<pk>[0-9]*)/?$', CheckoutSessionCreatingView.as_view(),
            name='create-checkout-session'),
    re_path(r'^item/(?P<pk>[0-9]*)/?$', ProductLandingPageView.as_view(), name='item-page'),
    re_path(r'^success/?$', SuccessView.as_view(), name='success-pay'),
    re_path(r'^cancel/?$', CancelView.as_view(), name='cancel-pay')
]
