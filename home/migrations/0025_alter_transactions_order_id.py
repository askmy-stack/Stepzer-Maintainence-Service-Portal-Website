# Generated by Django 3.2 on 2021-11-12 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0024_auto_20211112_2328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='order_id',
            field=models.CharField(max_length=1000, null=True, unique=True),
        ),
    ]