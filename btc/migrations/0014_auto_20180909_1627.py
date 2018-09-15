# Generated by Django 2.1 on 2018-09-09 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('btc', '0013_auto_20180908_1309'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exchanges',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('m_name', models.CharField(default='none', max_length=30)),
                ('m_website', models.CharField(max_length=20, null=True)),
                ('m_area', models.CharField(max_length=10, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='coinbar',
            name='m_area',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
