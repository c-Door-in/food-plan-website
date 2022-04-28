from django.shortcuts import render

from .models import Dish, Product, Subscribe, User, Preference, Allergy, Bill


def mainpage(request):
    return render(request, 'index.html')


def cardpage(request):
    first_dish = Dish.objects.all()[0]
    template_name = 'card3.html'
    context = {
        'title': first_dish.title,
        'image_url': f'https://www.kuharka.ru{first_dish.image_url}',
        'instruction': first_dish.instruction,
        'ingredients': first_dish.ingredients.all(),
    }
    return render(request, template_name, context)

