# Generated by Django 5.1.1 on 2025-01-07 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.TextField(blank=True, primary_key=True, serialize=False)),
                ('writer', models.TextField(blank=True, default='')),
                ('writedate', models.TextField(blank=True, default='')),
                ('content', models.TextField(blank=True, default='')),
            ],
            options={
                'managed': True,
            },
        ),
    ]
