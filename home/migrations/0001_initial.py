# Generated by Django 3.2 on 2021-10-24 14:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='members',
            fields=[
                ('member_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('block', models.CharField(choices=[('L1', 'L1'), ('L2', 'L2')], max_length=5)),
                ('flat', models.IntegerField()),
                ('flat_type', models.CharField(choices=[('O', 'owner'), ('R', 'Rent'), ('E', 'Empty')], max_length=1)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]