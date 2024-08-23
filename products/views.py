from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.core.cache import cache

# Create your views here.

from products.models import Product, ProductCategory, Tag, Basket
from users.models import User
from common.views import TitleMixin


# використовуємо Mixin
class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'


# # перевизначаємо метод для додавання Title
#     def get_context_data(self, **kwargs):
#         context = super(IndexView, self).get_context_data()
#         context['title'] = 'Store'
#         return context


class ProductListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3
    title = 'Store - Каталог'

    def get_queryset(self):
        queryset = super(ProductListView, self).get_queryset().order_by('id')
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data()
        categories = cache.get('categories')
        if not categories:
            context['categories'] = ProductCategory.objects.all()
            cache.set('categories', context['categories'], timeout=30)
        else:
            context['categories'] = categories
        # context['tags'] = Tag.objects.all()
        return context

# переходимо з FBV на CBV

# def index(request):
#     context = {
#         'title': 'Home',
#         'is_promotion': False,
#     }
#     return render(request, 'products/index.html', context)


# def products(request, category_id=None, page_number=1):
#     if category_id:
#         products = Product.objects.filter(category_id=category_id)
#     else:
#         products = Product.objects.all()
#     paginator = Paginator(products, per_page=3)
#     products_paginator = paginator.page(page_number)
#
#     context = {
#         'title': 'Shop - Каталог',
#         'categories': ProductCategory.objects.all(),
#         'products': products_paginator,
#         'tags': Tag.objects.all(),
#     }
#     return render(request, 'products/products.html', context)


@login_required  # декоратор для того, щоб не було корзини у незалогінених користувачів
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
