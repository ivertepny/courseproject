from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.core.cache import cache

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

from products.models import Product, ProductCategory, Tag, Basket
from users.models import User
from common.views import TitleMixin


# використовуємо Mixin
class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'


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


@login_required  # декоратор для того, щоб не було корзини у незалогінених користувачів
def basket_add(request, product_id):
    Basket.create_or_update(product_id, request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


# Зміна кільності листівок безпосередьно з кошика
@login_required
def basket_update(request, basket_id):
    basket = get_object_or_404(Basket, id=basket_id, user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    basket.quantity = quantity
    basket.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
