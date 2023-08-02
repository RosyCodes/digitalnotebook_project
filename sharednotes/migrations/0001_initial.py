# Generated by Django 4.2.2 on 2023-07-25 00:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import secrets


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notes', '0005_alter_note_main_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='SharedNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(default=secrets.token_urlsafe, max_length=32, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('note', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notes.note')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]