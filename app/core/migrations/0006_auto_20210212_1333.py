# Generated by Django 3.1.6 on 2021-02-12 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_transacao_tipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transacao',
            name='valor',
            field=models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Valor'),
        ),
    ]
