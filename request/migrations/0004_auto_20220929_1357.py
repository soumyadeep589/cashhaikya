# Generated by Django 3.2.10 on 2022-09-29 13:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("request", "0003_auto_20220927_1806"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="request",
            name="user",
        ),
        migrations.AddField(
            model_name="request",
            name="closed_to",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="closed_requests",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="request",
            name="opened_by",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="opened_requests",
                to="user.customuser",
            ),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name="CallList",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                (
                    "called_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "request",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="request.request",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "call_list",
                "db_table": "call_list",
                "ordering": ["id"],
                "unique_together": {("request", "called_by")},
            },
        ),
    ]
