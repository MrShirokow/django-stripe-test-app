from django.contrib import admin

from stripe_payment.models.item import Item
from stripe_payment.models.order import Order


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'display_price')
    list_display_links = list_display


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_cost')
    list_display_links = list_display
