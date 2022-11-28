from django.contrib import admin

from stripe_payment.models.item import Item
from stripe_payment.models.order import Order
from stripe_payment.models.order_item import OrderItem


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'display_price')
    list_display_links = ('id', 'name')


class OrderItemInline(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_cost')
    list_display_links = list_display
    inlines = [
        OrderItemInline,
    ]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'item', 'quantity', 'display_cost')
    list_display_links = ('id', 'order', 'item')
