# Generated by Django 4.1.3 on 2024-01-31 08:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('outgo', '0012_remove_sheetitem_is_required'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='outgodata',
            options={'ordering': ('-outgo_date',), 'verbose_name': 'Расход', 'verbose_name_plural': 'Расходы'},
        ),
        migrations.AlterField(
            model_name='subdivision',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь (владелец)'),
        ),
    ]
