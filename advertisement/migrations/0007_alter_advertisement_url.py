# Generated by Django 3.2 on 2022-01-21 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0006_alter_crawlerconfig_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='url',
            field=models.TextField(unique=True),
        ),
    ]
