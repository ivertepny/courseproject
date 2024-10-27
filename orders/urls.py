# Мій файл urls

from django.urls import path

from orders.views import OrderCreateView, SuccessTemplateView, CanceledTemplateView, OrderListView, OrderDetailView, \
    send_orders_to_google_sheet

app_name = 'orders'  # Не зрозумів для чого

urlpatterns = [
    path('order-create/', OrderCreateView.as_view(), name='order_create'),
    path('', OrderListView.as_view(), name='orders_list'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order'),
    path('order-success/', SuccessTemplateView.as_view(), name='order_success'),
    path('order-canceled/', CanceledTemplateView.as_view(), name='order_canceled'),
    path('send-to-google-sheet/', send_orders_to_google_sheet, name='send_to_google_sheet'),

]
