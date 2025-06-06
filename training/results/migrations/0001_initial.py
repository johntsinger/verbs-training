# Generated by Django 5.1.1 on 2025-02-27 09:57

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
        ('tables', '0001_initial'),
        ('verbs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('is_success', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='profiles.profile')),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='tables.table')),
                ('verb', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='verbs.verb')),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('owner', 'table', 'verb'), name='unique_result_for_verb_in_table_per_owner')],
            },
        ),
    ]
