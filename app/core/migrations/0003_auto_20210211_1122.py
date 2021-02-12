# Generated by Django 3.1.6 on 2021-02-11 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210210_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conta',
            name='limiteSaqueDiario',
            field=models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Limite de Saque Diário'),
        ),
        migrations.AlterField(
            model_name='conta',
            name='saldo',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='Saldo'),
        ),
    ]
