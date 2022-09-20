from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'producs'
        ordering = ['id']
        app_label = 'stripe_payment'

    def __str__(self):
        return f'{self.name}: {self.price}'
