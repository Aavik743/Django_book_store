# Generated by Django 4.0.5 on 2022-07-13 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_alter_book_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='is_on_wishlist',
            field=models.BooleanField(default=False),
        ),
    ]
