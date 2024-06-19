# Generated by Django 5.0.1 on 2024-06-19 06:44

import django.db.models.deletion
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
            name='DefaultTable',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_available', models.BooleanField(default=True)),
                ('verbs', models.ManyToManyField(related_name='%(class)s', to='verbs.verb')),
            ],
        ),
        migrations.CreateModel(
            name='UserTable',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usertables', to='profiles.profile')),
                ('verbs', models.ManyToManyField(related_name='%(class)s', to='verbs.verb')),
            ],
        ),
        migrations.AddConstraint(
            model_name='defaulttable',
            constraint=models.UniqueConstraint(fields=('name',), name='tables_defaulttable_unique_name'),
        ),
        migrations.AddConstraint(
            model_name='usertable',
            constraint=models.UniqueConstraint(fields=('name', 'profile'), name='tables_usertable_unique_name_per_profile'),
        ),
    ]
