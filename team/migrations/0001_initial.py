# Generated by Django 3.0.5 on 2020-05-26 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='组名')),
            ],
            options={
                'verbose_name': '分组',
                'verbose_name_plural': '分组',
            },
        ),
    ]
