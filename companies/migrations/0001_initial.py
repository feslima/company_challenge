# Generated by Django 4.0.2 on 2022-02-14 13:40

import core.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', core.fields.PrimaryKeyUUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('cnpj', core.fields.CNPJField(help_text='Format: 00.000.000/0001-00.', max_length=18, unique=True, verbose_name='CNPJ')),
                ('corporate_name', models.CharField(max_length=100)),
                ('trading_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', core.fields.PrimaryKeyUUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date_joined', models.DateTimeField(auto_now_add=True, help_text='When the user joined the company', verbose_name='date joined')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='companies.company')),
            ],
        ),
    ]
