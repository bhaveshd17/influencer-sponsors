# Generated by Django 3.2.7 on 2021-11-09 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20211109_2123'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsored',
            name='sponsor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.sponsor'),
            preserve_default=False,
        ),
    ]