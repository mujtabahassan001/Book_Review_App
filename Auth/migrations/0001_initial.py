# Generated by Django 5.1.4 on 2024-12-18 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Auth',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
    ]
