# Generated by Django 3.2.7 on 2021-11-09 12:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsored',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.influencerpost'),
        ),
    ]