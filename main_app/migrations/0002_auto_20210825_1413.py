# Generated by Django 3.2.5 on 2021-08-25 19:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(verbose_name='Date of purchase')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('notes', models.TextField(max_length=100)),
                ('category', models.CharField(max_length=100)),
                ('retailer', models.CharField(max_length=100)),
                ('budget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.budget')),
            ],
        ),
    ]
