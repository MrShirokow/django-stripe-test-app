from django.urls import re_path

from stripe_payment.views import buy, get_item


urlpatterns = [
    re_path(r'^buy/(?P<id>[0-9]*)/?$', buy, name='buy-item'),
    re_path(r'^item/(?P<id>[0-9]*)/?$', get_item, name='get-item'),
]
