import os
import re
import base64
import time

from io import BytesIO

from openai import OpenAI, OpenAIError

from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.http import JsonResponse

from PIL import Image
from postcards_shop import settings
from products.models import Product, ProductCategory, Basket  # , Tag
from common.views import TitleMixin
from .connect_mongodb import connect_mongo
from .documents import ProductDocument


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
        popular_product_ids = [str(product['product_id']) for product in connect_mongo().find({})]
        context['popular_product_ids'] = popular_product_ids

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


# Пошук за допомогою Elasticsearch з виділенням маркером
def highlight_search_term(text, query):
    # Екрануємо пошуковий запит для безпечної заміни в HTML
    highlighted_text = re.sub(
        f'({re.escape(query)})',
        r'<span style="background-color: red; color: white;">\1</span>', text, flags=re.IGNORECASE)
    return format_html(highlighted_text)  # повертаємо безпечний HTML


class ProductSearchListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/search.html'
    paginate_by = 3
    title = 'Store - Пошук'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            # Використовуємо Elasticsearch для пошуку продуктів
            s = ProductDocument.search().query("multi_match", query=query, fields=["name", "description"])
            return s.to_queryset()  # Повертаємо Django QuerySet з результатами

        return Product.objects.none()  # Повертаємо порожній QuerySet, якщо запит не було

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')  # Додаємо запит для шаблону
        context['products'] = self.get_queryset()  # Переконайтеся, що products завжди в контексті

        # Виділення в результатах
        if context['products']:
            for product in context['products']:
                product.name = highlight_search_term(product.name, context['query'])
                product.description = highlight_search_term(product.description, context['query'])
        return context


class PopularProductsView(TitleMixin, ListView):
    model = Product
    template_name = 'products/popular_products.html'
    paginate_by = 3
    title = 'Store - Популярні Продукти'

    def get_queryset(self):
        popular_products = cache.get('popular_products')
        popular_products = list(connect_mongo().find({}))
        # Кешуємо на 30 хвилин
        cache.set('popular_products', popular_products, timeout=1800)

        return popular_products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_products'] = self.get_queryset()
        return context


# OpenAI

class TextToImageView(TemplateView):
    template_name = 'products/text_to_image.html'
    title = 'Store - AI'

    def post(self, request, *args, **kwargs):
        text_prompt = request.POST.get("prompt")
        if not text_prompt:
            return JsonResponse({"error": "No text prompt provided."}, status=400)

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return JsonResponse({"error": "API key not configured."}, status=500)

        openai_client = OpenAI(api_key=api_key)

        try:
            response = openai_client.images.generate(
                model="dall-e-3",
                prompt=text_prompt,
                n=1,
                size="1024x1024",
                response_format="b64_json",
            )

            # Декодуємо image і підганяємо під розмір листівки
            image_data = response.data[0].b64_json
            decoded_image_data = base64.b64decode(image_data)
            image = Image.open(BytesIO(decoded_image_data))
            image = image.resize((458, 458))

            # Зберігаємо image
            filename = "generated_image_{}.jpg".format(int(time.time()))
            # file_path = os.path.join(settings.DEFAULT_FILE_STORAGE, filename)
            file_path = os.path.join(settings.MEDIA_ROOT, filename)
            image.save(file_path, "JPEG")


            # Генеруємо image URL
            image_url = os.path.join(settings.MEDIA_URL, filename)

            # Render response with context
            context = self.get_context_data(prompt=text_prompt, image_url=image_url)
            return self.render_to_response(context)

        except OpenAIError as e:
            if 'billing_hard_limit_reached' in str(e):
                return JsonResponse({"error": "Billing limit reached. Please check your OpenAI billing settings."}, status=402)
            return JsonResponse({"error": str(e)}, status=500)
        except Exception as e:
            # Generic error handling
            return JsonResponse({"error": str(e)}, status=500)