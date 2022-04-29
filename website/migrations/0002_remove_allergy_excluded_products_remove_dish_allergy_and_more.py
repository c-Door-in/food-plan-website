# Generated by Django 4.0.4 on 2022-04-29 13:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allergy',
            name='excluded_products',
        ),
        migrations.RemoveField(
            model_name='dish',
            name='allergy',
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название категории')),
                ('allergies', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='inappropriate_categories', to='website.allergy', verbose_name='Не подходит для')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.AddField(
            model_name='dish',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dishes', to='website.category', verbose_name='Категория блюда'),
        ),
    ]
