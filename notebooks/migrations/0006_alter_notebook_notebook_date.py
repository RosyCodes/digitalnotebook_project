# Generated by Django 4.2.2 on 2023-08-04 01:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('notebooks', '0005_rename_user_id_notebook_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notebook',
            name='notebook_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
