# Generated by Django 2.1 on 2018-08-26 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('btc', '0002_auto_20180826_0842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coinexchanges',
            name='m_area',
            field=models.CharField(default='unknown', max_length=10),
        ),
        migrations.AlterField(
            model_name='coinexchanges',
            name='m_exchange',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='coinexchanges',
            name='m_name',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='coinexchanges',
            name='m_website',
            field=models.CharField(max_length=20),
        ),
    ]
