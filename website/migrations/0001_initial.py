# Generated by Django 4.0.4 on 2022-04-29 10:21

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Allergy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Аллергия')),
                ('excluded_products', models.TextField(null=True, verbose_name='Исключенные продукты')),
            ],
            options={
                'verbose_name': 'Аллергия',
                'verbose_name_plural': 'Аллергии',
            },
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название блюда')),
                ('instruction', models.TextField(verbose_name='Способ приготовления')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Изображение')),
                ('image_url', models.TextField(blank=True, verbose_name='Ссылка на картинку')),
                ('calories', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Калорийность')),
                ('allergy', models.ManyToManyField(related_name='inappropriate_dishes', to='website.allergy', verbose_name='Не подходит для:')),
            ],
            options={
                'verbose_name': 'Блюдо',
                'verbose_name_plural': 'Блюда',
            },
        ),
        migrations.CreateModel(
            name='Preference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Предпочтения')),
            ],
            options={
                'verbose_name': 'Предпочтение',
                'verbose_name_plural': 'Предпочтения',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название продукта')),
            ],
            options={
                'verbose_name': 'Ингридиент',
                'verbose_name_plural': 'Ингридиенты',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=250, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=250, verbose_name='Фамилия')),
                ('chat_id', models.IntegerField(unique=True, verbose_name='Chat id')),
                ('phone', models.CharField(blank=True, max_length=20, verbose_name='Номер телефона')),
                ('favorite_dishes', models.ManyToManyField(blank=True, default=None, related_name='favourite', to='website.dish', verbose_name='Любимые блюда')),
                ('unloved_dishes', models.ManyToManyField(blank=True, default=None, related_name='unloved', to='website.dish', verbose_name='Нелюбимые блюда')),
            ],
            options={
                'verbose_name': 'Подписчик',
                'verbose_name_plural': 'Подписчики',
            },
        ),
        migrations.CreateModel(
            name='Subscribe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('number_of_meals', models.PositiveSmallIntegerField(verbose_name='Количество приемов пищи в день')),
                ('persons_quantity', models.PositiveSmallIntegerField(default=1, verbose_name='Количество человек, на которых должна быть рассчитана порция')),
                ('sub_type', models.CharField(choices=[('1', '1'), ('3', '3'), ('6', '6'), ('9', '9'), ('12', '12')], db_index=True, default=12, max_length=25, verbose_name='Тип подписки')),
                ('subscription_start', models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Подписка была приобретена')),
                ('allergy', models.ManyToManyField(blank=True, related_name='subscribes', to='website.allergy', verbose_name='Аллергии')),
                ('preference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribes', to='website.preference', verbose_name='Предпочтения')),
                ('shown_dishes', models.ManyToManyField(blank=True, related_name='used_subscribes', to='website.dish', verbose_name='Показанные блюда')),
                ('subscriber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribes', to='website.user', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Подписка',
                'verbose_name_plural': 'Подписки',
            },
        ),
        migrations.AddField(
            model_name='dish',
            name='ingredients',
            field=models.ManyToManyField(related_name='dishes', to='website.product', verbose_name='Ингредиенты'),
        ),
        migrations.AddField(
            model_name='dish',
            name='preferences',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='appropriate_dishes', to='website.preference', verbose_name='Подходит для:'),
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(db_index=True, verbose_name='Стоимость заказа')),
                ('creation_date', models.DateTimeField(db_index=True, verbose_name='Дата создания заказа')),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscription', to='website.subscribe', verbose_name='Относится к подписке')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='website.user', verbose_name='Чек пользователя')),
            ],
            options={
                'verbose_name': 'Продажа',
                'verbose_name_plural': 'Продажи',
            },
        ),
    ]
