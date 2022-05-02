from datetime import datetime, timedelta, time

from django.contrib.auth.models import User
from django.contrib.postgres.fields import DateTimeRangeField
from django.db import models
from django.utils.timezone import now


class Preference(models.Model):
    title = models.CharField('Предпочтения', max_length=200)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Предпочтение'
        verbose_name_plural = 'Предпочтения'


class Allergy(models.Model):
    title = models.CharField('Аллергия', max_length=200)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Аллергия'
        verbose_name_plural = 'Аллергии'


class Product(models.Model):
    title = models.CharField('Название продукта', max_length=200)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'


class Category(models.Model):
    title = models.CharField('Название категории', max_length=200)
    allergy = models.ForeignKey(
        Allergy,
        verbose_name='Не подходит для',
        related_name='inappropriate_categories',
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Dish(models.Model):
    title = models.CharField('Название блюда', max_length=200)
    instruction = models.TextField('Способ приготовления')
    image = models.ImageField(
        "Изображение",
        null=True,
        blank=True,
    )
    image_url = models.TextField(
        'Ссылка на картинку',
        blank=True,
    )
    ingredients = models.ManyToManyField(
        Product,
        verbose_name='Ингредиенты',
        related_name='dishes',
    )
    preferences = models.ForeignKey(
        Preference,
        verbose_name='Подходит для:',
        related_name='appropriate_dishes',
        on_delete=models.SET_NULL,
        null=True,
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория блюда',
        related_name='dishes',
        on_delete=models.SET_NULL,
        null=True,
    )
    calories = models.PositiveSmallIntegerField(
        'Калорийность',
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'


# class User(models.Model):
#     first_name = models.CharField('Имя', max_length=250)
#     last_name = models.CharField('Фамилия', max_length=250, blank=True)
#     chat_id = models.IntegerField('Chat id', unique=True)
#     phone = models.CharField('Номер телефона', max_length=20, blank=True)
#     favorite_dishes = models.ManyToManyField(Dish,
#                                              verbose_name='Любимые блюда',
#                                              related_name='favourite',
#                                              blank=True,
#                                              default=None)
#
#     unloved_dishes = models.ManyToManyField(Dish,
#                                             verbose_name='Нелюбимые блюда',
#                                             related_name='unloved',
#                                             blank=True,
#                                             default=None)
#
#     def __str__(self):
#         return f'ID: {self.chat_id} имя: {self.first_name} телефон: {self.phone}'
#
#     class Meta:
#         verbose_name = 'Подписчик'
#         verbose_name_plural = 'Подписчики'


class Subscribe(models.Model):
    title = models.CharField('Название', max_length=200)

    SubscribeLengthChoices = (
        ('1', '1'),
        ('3', '3'),
        ('6', '6'),
        ('9', '9'),
        ('12', '12')
    )

    subscriber = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='subscribes',
        on_delete=models.CASCADE,
    )
    preference = models.ForeignKey(
        Preference,
        verbose_name='Предпочтения',
        related_name='subscribes',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    allergy = models.ManyToManyField(
        Allergy,
        verbose_name='Аллергии',
        related_name='subscribes',
        blank=True,
    )
    number_of_meals = models.PositiveSmallIntegerField(
        'Количество приемов пищи в день',
    )

    persons_quantity = models.PositiveSmallIntegerField(
        'Количество человек, на которых должна быть рассчитана порция',
        default=1
    )
    sub_type = models.CharField(
        'Тип подписки',
        choices=SubscribeLengthChoices,
        db_index=True,
        default=12,  # TODO в случае ошибки скрипта, пользователь автоматически получает максимальную подписку!!!
        max_length=25,
    )
    subscription_start = models.DateTimeField(
        # TODO do not allow blank!
        'Подписка была приобретена',
        default=now,
    )

    def __str__(self):
        return f'Подписка {self.pk} - {self.title} - {self.subscriber.first_name}'

    def select_available_dishes(self):
        allergens = [allergy for allergy in Allergy.objects.all()]
        preference = self.preference
        available_dishes = Dish.objects.filter(preferences=preference) \
                             .exclude(category__allergy__in=allergens)
        self.available_dishes = available_dishes

        return self.available_dishes

    def get_planned_dish_id(self):
        available_dishes = self.select_available_dishes()
        dish_index = 0
        time_ranges = {
            1: [(5, 23)],
            2: [(5, 14), (15, 23)],
            3: [(5, 11), (12, 17), (18, 23)],
            4: [(5, 9), (10, 14), (15, 19), (20, 23)],
        }
        now = datetime.now()
        for day in range(int(self.sub_type) * 30):
            current_date = self.subscription_start + timedelta(day)
            if current_date.date() == now.date():
                for hour_range in time_ranges[self.number_of_meals]:
                    if dish_index+1 > len(available_dishes):
                        dish_index = 0
                    if now.hour in range(*hour_range):
                        return available_dishes[dish_index].id
                    dish_index += 1
                return 'wrongtime'
            dish_index += self.number_of_meals
        return None

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class Bill(models.Model):

    price = models.IntegerField(
        'Стоимость заказа',
        db_index=True,
    )
    user = models.ForeignKey(
        User,
        verbose_name='Чек пользователя',
        related_name='user',
        on_delete=models.CASCADE
    )
    subscription = models.ForeignKey(
        Subscribe,
        verbose_name='Относится к подписке',
        related_name='subscription',
        on_delete=models.CASCADE
    )
    creation_date = models.DateTimeField(
        'Дата создания заказа',
        db_index=True
    )

    def __str__(self):
        return f'Чек пользователя {self.user.first_name}'

    class Meta:
        verbose_name = 'Продажа'
        verbose_name_plural = 'Продажи'
