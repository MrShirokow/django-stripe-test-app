from django.contrib import admin

from stripe_payment.models.item import Item
from stripe_payment.models.order import Order


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'price')
    list_display_links = list_display


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', )
    list_display_links = list_display
