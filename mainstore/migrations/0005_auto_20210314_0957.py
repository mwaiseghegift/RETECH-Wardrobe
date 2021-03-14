# Generated by Django 3.1.7 on 2021-03-14 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainstore', '0004_category_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        migrations.AddField(
            model_name='manufacture',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        migrations.AddField(
            model_name='upcoming_product',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]