from django.db import models

from .item import Item


class Order(models.Model):
    cost = models.IntegerField(default=0)
    items = models.ManyToManyField(Item)

    @property
    def display_cost(self):
        return f'{self.cost / 100:.2f}'

    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'
        ordering = ['id']
        app_label = 'stripe_payment'
