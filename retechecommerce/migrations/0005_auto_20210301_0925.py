# Generated by Django 3.1.6 on 2021-03-01 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retechecommerce', '0004_upcoming_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='upcoming_product',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
