import json
import os
from urllib.parse import urlsplit, unquote

import requests

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from website.models import Dish, Product, Allergy, Preference


def upload_image(image_url, title):
    dish = Dish.objects.get(title=title)
    name = os.path.basename(unquote(urlsplit(image_url).path))

    image_response = requests.get(image_url)
    image_response.raise_for_status()
    image_content = ContentFile(image_response.content)

    dish.image.save(
        name,
        image_content,
        save=True
    )


def add_to_db(recipe):
    title = recipe['title']
    instruction = recipe['instruction']
    image_url = recipe['image_url']
    ingredients = recipe['ingredients']
    comments = recipe['comments']

    # image_response = requests.get(image_url)
    # image_response.raise_for_status()
    # image_content = ContentFile(image_response.content)

    dish, created = Dish.objects.get_or_create(
        title=title,
        defaults={
            'instruction': instruction,
            'image_url': image_url,
            'preferences': None,
        }
    )

    upload_image(image_url, title)

    for ingredient in ingredients:
        # formatted_product = ingredient.split(' – ')[0] if ' - ' in ingredient else ingredient
        prod, created = Product.objects.get_or_create(
            title=ingredient)
        dish.ingredients.add(prod)

    print(f'Добавлено блюдо: "{title}"')


def main():
    with open(f'media/recipes_fixed.json', 'r', encoding='utf-8') as source:
        recipes = json.load(source)
    for recipe in recipes:
        add_to_db(recipe)


class Command(BaseCommand):
    help = 'Внести данные из json в базу данных'

    def handle(self, *args, **options):
        main()
