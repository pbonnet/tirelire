# Generated by Django 4.2 on 2023-04-07 19:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_add_eur_cash_data'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cash',
            options={'ordering': ['value']},
        ),
    ]