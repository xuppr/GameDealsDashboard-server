# Generated by Django 3.2.5 on 2021-07-29 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0004_alter_deal_dealrating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deal',
            name='dealID',
            field=models.CharField(default='1', max_length=255, unique=True),
        ),
    ]
