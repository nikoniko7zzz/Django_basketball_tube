# Generated by Django 4.1.1 on 2022-10-02 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='birth_day',
            field=models.DateField(blank=True, null=True),
        ),
    ]