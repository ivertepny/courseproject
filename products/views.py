from django.shortcuts import render

# Create your views here.

from products.models import Product, ProductCategory, Tag


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
        # 'tags': Tag.objects.all(),

    }
    
    return render(request, 'products/products.html', context)
