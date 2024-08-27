"""
URL configuration for postcards_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
# from products.views import index
from products.views import IndexView
from orders.views import stripe_webhook_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),

    path('products/', include('products.urls', namespace='products')),

    path('users/', include('users.urls', namespace='users')),
    path('accounts/', include('allauth.urls')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('webhook/stripe/', stripe_webhook_view, name='stripe_webhook'),
]

if settings.DEBUG:
    urlpatterns.append(path('__debug__/', include("debug_toolbar.urls")))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
