# Generated by Django 5.0.1 on 2024-06-19 06:44

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
                ('default_table', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='results', to='tables.defaulttable')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='profiles.profile')),
                ('user_table', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='results', to='tables.usertable')),
                ('verb', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='verbs.verb')),
            ],
        ),
        migrations.AddConstraint(
            model_name='result',
            constraint=models.CheckConstraint(check=models.Q(('default_table__isnull', True), ('user_table__isnull', True), _connector='XOR'), name='results_result_only_default_table_or_user_table_must_be_set'),
        ),
    ]
