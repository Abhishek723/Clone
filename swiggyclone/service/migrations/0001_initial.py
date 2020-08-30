# Generated by Django 3.1 on 2020-08-29 13:35

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('address', models.TextField(max_length=500)),
                ('pincode', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch', models.IntegerField()),
                ('foodItem', models.IntegerField()),
                ('order_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('total_price', models.IntegerField(default=0)),
                ('quantity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Restaurent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('discription', models.TextField(blank=True, max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='FoodItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('price', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.branch')),
            ],
        ),
        migrations.AddField(
            model_name='branch',
            name='restaurent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.restaurent'),
        ),
    ]