# Generated by Django 5.1.1 on 2024-09-29 01:36

import django.core.validators
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(db_comment='Item name.', max_length=128)),
                ('description', models.TextField(blank=True, db_comment='Item description.')),
                ('gross_cost', models.DecimalField(db_comment='Item cost before deductions and taxes.', decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(Decimal('0'))])),
                ('tax_applicable', models.DecimalField(db_comment='Taxes applicable to the item.', decimal_places=2, max_digits=3, validators=[django.core.validators.MaxValueValidator(Decimal('1'))])),
                ('reference', models.CharField(blank=True, db_comment='Item reference', max_length=128)),
            ],
            options={
                'db_table': 'items',
            },
        ),
    ]
