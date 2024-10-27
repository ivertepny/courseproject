import stripe
from http import HTTPStatus
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy, reverse
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from common.views import TitleMixin
from google_sheet.service import write_orders_to_sheet

from orders.forms import OrderForm
from products.models import Basket
from orders.models import Order
from telegrambot.tasks import send_telegram

# Stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Shop - Дякуємо за замовлення!'


class CanceledTemplateView(TemplateView):
    template_name = 'orders/canceled.html'


class OrderListView(TitleMixin, ListView):
    template_name = 'orders/orders.html'
    title = 'Shop - Замовлення'
    queryset = Order.objects.all()
    ordering = ('-created_at',)

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        return queryset.filter(initiator=self.request.user)


class OrderDetailView(DetailView):
    template_name = 'orders/order.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['title'] = f"Store - Замовлення №{self.object.id} "
        return context


class OrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')
    title = 'Store - Оформлення замовлення'

    # stripe
    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        baskets = Basket.objects.filter(user=self.request.user)
        checkout_session = stripe.checkout.Session.create(
            line_items=baskets.stripe_products(),
            metadata={'order_id': self.object.id},
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_success')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_canceled')),
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)


# Use the secret provided by Stripe CLI for local testing
# or your webhook endpoint's secret.

@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Fulfill the purchase...
        fulfill_order(session)
        # надсилає повідомлення в Телеграм через Celery
        send_telegram.delay()

    # Passed signature verification
    return HttpResponse(status=200)


def fulfill_order(session):
    order_id = int(session.metadata.order_id)
    order = Order.objects.get(id=order_id)
    order.update_after_payment()


@login_required
def send_orders_to_google_sheet(request):
    user = request.user  # Отримати поточного користувача
    write_orders_to_sheet('18wo-GwoHlmPPjTD4M3wVeS28q0qOPRfh57xLCgMkh1E', user, 'A1:E100')
    # return redirect('orders:orders_list')
    return redirect('https://docs.google.com/spreadsheets/d/18wo-GwoHlmPPjTD4M3wVeS28q0qOPRfh57xLCgMkh1E/edit?gid=0#gid=0')
