# Generated by Django 3.2.6 on 2021-08-30 15:36

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_auto_20210827_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
