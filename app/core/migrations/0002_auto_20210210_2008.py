# Generated by Django 3.1.6 on 2021-02-10 20:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='conta',
            unique_together={('idPessoa', 'tipoConta')},
        ),
    ]
