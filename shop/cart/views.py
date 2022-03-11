from django.http import HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from main.models import Product
from .cart import Cart
from .forms import *
from main.models import Category


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])

    return redirect('cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request)
    categories = Category.objects.all()
    return render(request, 'cart/shop-cart.html', {'cart': cart, 'categories': categories, 'title': "Cart"})


def shop_checkout(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # очистка корзины
            cart.clear()
            return HttpResponseRedirect(reverse('cart_detail'))
    else:
        form = OrderCreateForm
    return render(request, 'cart/shop-checkout.html', {'cart': cart, 'form': form})
