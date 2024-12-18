# Generated by Django 5.0.6 on 2024-11-18 10:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="posts",
            old_name="likes",
            new_name="like_count",
        ),
        migrations.AlterField(
            model_name="likes",
            name="post",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="likes",
                to="network.posts",
            ),
        ),
        migrations.AlterField(
            model_name="likes",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="liked_posts",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="posts",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="posts",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
