# Generated by Django 3.2.6 on 2021-08-30 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_alter_budget_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
