# Generated by Django 4.2 on 2023-04-25 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_image', models.URLField()),
                ('title', models.CharField(max_length=250)),
                ('year', models.IntegerField()),
                ('rating', models.FloatField()),
            ],
        ),
    ]
