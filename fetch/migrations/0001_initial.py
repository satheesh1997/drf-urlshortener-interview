# Generated by Django 2.0.1 on 2018-03-17 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shorturl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('long_url', models.URLField()),
                ('short_url', models.CharField(max_length=8)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
    ]
