# Generated by Django 4.2.2 on 2023-07-25 20:01

from django.db import migrations, models
import secrets


class Migration(migrations.Migration):

    dependencies = [
        ('sharednotes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sharednote',
            name='token',
            field=models.CharField(default=secrets.token_urlsafe, max_length=150, unique=True),
        ),
    ]
