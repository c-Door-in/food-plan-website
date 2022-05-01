from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.urls import reverse

from website.models import Dish


def mainpage(request):
    return render(request, 'index.html')


def get_allergies(order_details):
    allergies = []
    for order_param, param_value in order_details.items():
        if 'allergy' in order_param:
            allergies.append(param_value)
    return allergies


def order(request):
    user_id = request.user.id
    if not user_id:
        return HttpResponseRedirect(reverse('login'))
    order_details = request.POST
    if order_details:
        request.session[f'sub_{str(user_id)}'] = {
            'subscriber': user_id,
            'allergies': get_allergies(order_details),
            'number_of_meals': sum([int(order_details['first_meal']),
                                   int(order_details['second_meal']),
                                   int(order_details['third_meal']),
                                   int(order_details['fourth_meal'])]),
            'persons_quantity': order_details['persons_quantity'],
            'sub_type': order_details['sub_type']
        }
        return HttpResponseRedirect(reverse('make_payment'))

    return render(request, 'order.html')


class CardView(DetailView):

    model = Dish
    template_name = 'card3.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

