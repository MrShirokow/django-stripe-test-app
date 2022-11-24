from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    price = models.IntegerField(default=0)

    @property
    def display_price(self):
        return f'{self.price / 100:.2f}'

    class Meta:
        verbose_name = 'item'
        verbose_name_plural = 'items'
        ordering = ['id']
        app_label = 'stripe_payment'

    def __str__(self) -> str:
        return f'Item: {self.name}: {self.display_price}'
