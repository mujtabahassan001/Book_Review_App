# Generated by Django 5.1.4 on 2024-12-18 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to='books-images/'),
        ),
    ]
