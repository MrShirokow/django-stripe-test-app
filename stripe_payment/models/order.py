from django.db import models

from .item import Item


class Order(models.Model):
    items = models.ManyToManyField(Item)

    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'
        ordering = ['id']
        app_label = 'stripe_payment'
