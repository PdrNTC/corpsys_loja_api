# Generated by Django 5.0 on 2024-09-30 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corpsys_loja', '0003_alter_venda_data_venda'),
    ]

    operations = [
        migrations.AddField(
            model_name='venda',
            name='valor_total_venda',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
