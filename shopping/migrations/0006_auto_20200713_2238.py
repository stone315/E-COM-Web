# Generated by Django 3.0.8 on 2020-07-13 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0005_auto_20200713_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='Time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]