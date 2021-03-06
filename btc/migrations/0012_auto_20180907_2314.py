# Generated by Django 2.1 on 2018-09-07 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('btc', '0011_auto_20180907_2307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coinbar',
            name='m_coin',
            field=models.CharField(default='none', max_length=10),
        ),
        migrations.AlterField(
            model_name='coinbar',
            name='m_name',
            field=models.CharField(default='none', max_length=30),
        ),
        migrations.AlterField(
            model_name='coinbar',
            name='m_symbol',
            field=models.CharField(default='none', max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='coinbar',
            name='m_updatetime',
            field=models.CharField(max_length=25, null=True),
        ),
    ]
