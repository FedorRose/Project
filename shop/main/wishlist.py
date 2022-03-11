import copy
from decimal import Decimal
from django.conf import settings
from .models import Product


class Wishlist(object):

    def __init__(self, request):
        self.session = request.session
        wishlist = self.session.get(settings.WISHLIST_SESSION_ID)
        if not wishlist:
            wishlist = self.session[settings.WISHLIST_SESSION_ID] = {}
        self.wishlist = wishlist

    def add(self, product):
        product_id = str(product.id)
        if product_id not in self.wishlist:
            self.wishlist[product_id] = {'quantity': 1, 'price': str(product.price)}
        self.save()

    def save(self):
        self.session[settings.WISHLIST_SESSION_ID] = self.wishlist
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.wishlist:
            del self.wishlist[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.wishlist.keys()
        products = Product.objects.filter(id__in=product_ids)
        wishlist = copy.deepcopy(self.wishlist)
        for product in products:
            wishlist[str(product.id)]['product'] = product
        for item in wishlist.values():
            item['price'] = Decimal(item['price'])
            yield item

    def list(self):
        product_ids = self.wishlist.keys()
        products = Product.objects.filter(id__in=product_ids)
        l = []
        for product in products:
            l.append(product)
        return l

    def clear(self):
        del self.session[settings.WISHLIST_SESSION_ID]
        self.session.modified = True
