from django.db import models


class Order(models.Model):

    @property
    def total_cost(self):
        return sum([item.total_cost for item in self.order_items.all()])

    @property
    def display_cost(self):
        return f'{self.total_cost / 100:.2f}'

    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'
        ordering = ['id']
        app_label = 'stripe_payment'

    def __str__(self) -> str:
        return f'Order #{self.id}: {self.display_cost}'
