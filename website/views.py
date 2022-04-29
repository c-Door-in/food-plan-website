from django.shortcuts import render
from django.views.generic.detail import DetailView

from website.models import Dish, Product, Subscribe, User, Preference, Allergy, Bill


def mainpage(request):
    return render(request, 'index.html')


class CardView(DetailView):

    model = Dish
    template_name = 'card3.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

