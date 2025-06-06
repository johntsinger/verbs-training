# Generated by Django 5.1.1 on 2025-02-27 09:57

import django.db.models.deletion
import django.db.models.functions.text
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
        ('verbs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('type', models.CharField(choices=[('defaulttable', 'Default Table'), ('usertable', 'User Table')], max_length=12)),
                ('name', models.CharField(max_length=30)),
                ('slug_name', models.SlugField()),
                ('is_available', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tables', to='profiles.profile')),
                ('verbs', models.ManyToManyField(related_name='tables', to='verbs.verb')),
            ],
        ),
        migrations.CreateModel(
            name='DefaultTable',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('tables.table',),
        ),
        migrations.CreateModel(
            name='UserTable',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('tables.table',),
        ),
        migrations.AddConstraint(
            model_name='table',
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower('name'), condition=models.Q(('type', 'defaulttable')), name='unique_default_table_name'),
        ),
        migrations.AddConstraint(
            model_name='table',
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower('name'), models.F('owner'), condition=models.Q(('type', 'usertable')), name='unique_table_name_per_profile'),
        ),
    ]
