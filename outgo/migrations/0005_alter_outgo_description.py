# Generated by Django 4.1.3 on 2024-01-22 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('outgo', '0004_alter_subdivision_subdivision_short_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outgo',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Фамилии'),
        ),
    ]
