# Generated by Django 3.2.10 on 2022-09-29 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0002_alter_customuser_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="transactions",
            field=models.IntegerField(default=0),
        ),
    ]
