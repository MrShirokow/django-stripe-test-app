from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    price = models.IntegerField(default=0)

    @property
    def display_price(self):
        return f'{self.price / 100:.2f}'

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        ordering = ['id']
        app_label = 'stripe_payment'

    def __str__(self):
        return f'{self.name}: {self.price}'

