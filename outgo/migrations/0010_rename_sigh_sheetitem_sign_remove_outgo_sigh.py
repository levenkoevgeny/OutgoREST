# Generated by Django 4.1.3 on 2024-01-24 12:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('outgo', '0009_sheetitem_sigh'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sheetitem',
            old_name='sigh',
            new_name='sign',
        ),
        migrations.RemoveField(
            model_name='outgo',
            name='sigh',
        ),
    ]
