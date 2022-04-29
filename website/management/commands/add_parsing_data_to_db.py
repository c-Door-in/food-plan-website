import json
import os
from pathlib import Path
from urllib.parse import urlsplit, unquote

import requests

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from website.models import Dish, Product, Allergy, Category


def upload_image(image_url, title):
    dish = Dish.objects.get(title=title)
    filename = os.path.basename(unquote(urlsplit(image_url).path))
    filepath = os.path.join('img', filename)

    image_response = requests.get(image_url)
    image_response.raise_for_status()
    image_content = ContentFile(image_response.content)

    dish.image.save(
        filepath,
        image_content,
        save=True
    )


def add_allergy_types():
    allergy_types = [
        'Рыба и морепродукты',
        'Мясо',
        'Зерновые',
        'Продукты пчеловодства',
        'Орехи и бобовые',
        'Молочные продукты',
    ]

    for type in allergy_types:
        Allergy.objects.get_or_create(
            title=type
        )


def add_to_db(recipe):
    title = recipe['title']
    instruction = recipe['instruction']
    image_url = recipe['image_url']
    ingredients = recipe['ingredients']
    category, _ = Category.objects.get_or_create(title=recipe['category'])
    comments = recipe['comments']

    dish, created = Dish.objects.get_or_create(
        title=title,
        defaults={
            'instruction': instruction,
            'image_url': image_url,
            'preferences': None,
            'category': category,
        }
    )

    # upload_image(image_url, title)

    for ingredient in ingredients:
        # formatted_product = ingredient.split(' – ')[0] if ' - ' in ingredient else ingredient
        prod, created = Product.objects.get_or_create(
            title=ingredient)
        dish.ingredients.add(prod)

    print(f'Добавлено блюдо: "{title}"')


def main():
    add_allergy_types()
    # Path('media/img').mkdir(parents=True, exist_ok=True)
    with open(f'media/recipes.json', 'r', encoding='utf-8') as source:
        recipes = json.load(source)
    for recipe in recipes:
        add_to_db(recipe)


class Command(BaseCommand):
    help = 'Внести данные из json в базу данных'

    def handle(self, *args, **options):
        main()
