# Generated by Django 3.2.7 on 2021-10-12 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20211011_0927'),
    ]

    operations = [
        migrations.AddField(
            model_name='influencerpost',
            name='day',
            field=models.IntegerField(blank=True, default=5, null=True),
        ),
        migrations.AddField(
            model_name='influencerpost',
            name='price',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='influencerpost',
            name='price_desc',
            field=models.TextField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='influencerpost',
            name='slug',
            field=models.SlugField(blank=True, max_length=1000, null=True),
        ),
    ]