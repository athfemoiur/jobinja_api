# Generated by Django 3.2 on 2022-01-21 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CrawlerConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('source', models.PositiveSmallIntegerField(choices=[(0, 'جابینجا'), (1, 'جاب ویژن'), (2, 'کوئرا')], default=0)),
                ('city', models.PositiveSmallIntegerField(choices=[(0, 'تهران'), (1, 'البرز'), (2, 'اصفهان')], default=0)),
                ('url', models.URLField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('source', models.PositiveSmallIntegerField(choices=[(0, 'جابینجا'), (1, 'جاب ویژن'), (2, 'کوئرا')], default=0)),
                ('url', models.URLField(unique=True)),
                ('crawled', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='advertisement',
            name='source',
            field=models.PositiveSmallIntegerField(choices=[(0, 'جابینجا'), (1, 'جاب ویژن'), (2, 'کوئرا')], default=0),
        ),
        migrations.AlterField(
            model_name='advertisement',
            name='remaining_days',
            field=models.CharField(blank=True, default='', max_length=32, verbose_name='remaining days'),
            preserve_default=False,
        ),
    ]
