# Generated by Django 2.1 on 2018-08-26 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('btc', '0003_auto_20180826_0907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coinexchanges',
            name='m_website',
            field=models.CharField(default='unknown', max_length=20),
        ),
    ]
