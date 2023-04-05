# Generated by Django 4.2 on 2023-04-05 17:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cash',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cash_type', models.CharField(choices=[('bill', 'Bill'), ('coin', 'Coin')], max_length=4)),
                ('currency', models.CharField(choices=[('EUR', '€')], default='EUR', max_length=3)),
                ('value', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='MoneyBox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='MoneyBoxContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('cash', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.cash')),
                ('money_box', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.moneybox')),
            ],
        ),
        migrations.AddField(
            model_name='moneybox',
            name='cashes',
            field=models.ManyToManyField(through='app.MoneyBoxContent', to='app.cash'),
        ),
    ]