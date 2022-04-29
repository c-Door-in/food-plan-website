import stripe
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.conf import settings


def make_payment(request):
    stripe.api_key = settings.STRIPE_PUBLISHABLE_KEY

    amount =  5000

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'rub',
                'product_data': {
                    'name': f'Ваш заказ №',
                },
                'unit_amount': amount,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri('success/'),
        cancel_url=request.build_absolute_uri('cancelled/'),
    )

    return redirect(session.url, code=303)


def pay_success(request):
    # order = Order.objects.get(id=order_id)
    # order.status = 'ORDER'
    # order.save()
    return render(request, "success.html")


class CancelledView(TemplateView):
    template_name = 'cancelled.html'


class OrderView(TemplateView):
    template_name = 'order.html'
