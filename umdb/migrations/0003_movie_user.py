# Generated by Django 4.2.5 on 2024-05-11 04:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("umdb", "0002_movie"),
    ]

    operations = [
        migrations.AddField(
            model_name="movie",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
