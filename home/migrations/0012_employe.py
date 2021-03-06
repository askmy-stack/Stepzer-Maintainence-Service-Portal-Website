# Generated by Django 3.2 on 2021-10-30 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_delete_employe'),
    ]

    operations = [
        migrations.CreateModel(
            name='employe',
            fields=[
                ('emp_id', models.IntegerField(primary_key=True, serialize=False)),
                ('emp_name', models.CharField(max_length=50)),
                ('Present', models.CharField(choices=[('Y', 'Yes'), ('N', 'No')], max_length=1)),
                ('Available', models.CharField(choices=[('Y', 'Yes'), ('N', 'No')], max_length=1)),
                ('phone', models.IntegerField(default=None)),
            ],
        ),
    ]
