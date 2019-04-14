# Generated by Django 2.2 on 2019-04-11 08:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pizza', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('best_pizza', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='championed_by', to='pizza.Pizza')),
                ('pizzas', models.ManyToManyField(related_name='restaurants', to='pizza.Pizza')),
            ],
        ),
    ]
