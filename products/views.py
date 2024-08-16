from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

from products.models import Product, ProductCategory, Tag, Basket
from users.models import User


def index(request):
    context = {
        'title': 'Home',
        'is_promotion': False,
    }
    return render(request, 'products/index.html', context)


def products(request):
    context = {
        'title': 'Shop - Каталог',
        'products': Product.objects.all(),
        'categories': ProductCategory.objects.all(),
        'tags': Tag.objects.all(),

    }
    return render(request, 'products/products.html', context)


@login_required #декоратор для того, щоб не було корзини у незалогінених користувачів
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
