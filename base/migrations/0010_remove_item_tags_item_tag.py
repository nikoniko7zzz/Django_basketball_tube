# Generated by Django 4.1.1 on 2022-10-12 13:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_alter_item_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='tags',
        ),
        migrations.AddField(
            model_name='item',
            name='tag',
            field=models.ForeignKey(default='game', on_delete=django.db.models.deletion.CASCADE, to='base.tag'),
            preserve_default=False,
        ),
    ]
