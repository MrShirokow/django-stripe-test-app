from django.shortcuts import get_object_or_404, render

from stripe_payment.models.item import Item


def buy(request, id):
    item = get_object_or_404(Item, pk=id)
    return render(request, 'index.html', {'id': id, 'name': item.name,
                                          'description': item.description, 'price': item.price})


def get_item(request, id):
    item = get_object_or_404(Item, pk=id)
    return render(request, 'index.html', {'id': id, 'name': item.name,
                                          'description': item.description, 'price': item.price})