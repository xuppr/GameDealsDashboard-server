# Generated by Django 3.2.5 on 2021-07-29 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0002_auto_20210728_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deal',
            name='normalPrice',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='deal',
            name='salePrice',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='deal',
            name='savings',
            field=models.FloatField(null=True),
        ),
    ]
