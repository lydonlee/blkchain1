# Generated by Django 2.1 on 2018-08-29 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('btc', '0004_auto_20180826_0908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coinexchanges',
            name='m_area',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='coinexchanges',
            name='m_website',
            field=models.CharField(max_length=20),
        ),
    ]