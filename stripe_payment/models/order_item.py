from django.db import models

from .item import Item
from .order import Order


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, related_name='order_items')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, related_name='order_items')
    quantity = models.IntegerField(default=0)

    @property
    def total_cost(self):
        try:
            cost = self.item.price * self.quantity
        except AttributeError:
            cost = 0
        return cost

    @property
    def display_cost(self):
        return f'{self.total_cost / 100:.2f}'

    class Meta:
        verbose_name = 'order_item'
        verbose_name_plural = 'order_items'
        ordering = ['id']
        app_label = 'stripe_payment'

    def __str__(self) -> str:
        return f'OrderItem #{self.id}: {self.display_cost}'
