# Generated by Django 5.0.1 on 2024-02-15 09:06

import json
from django.db import migrations


def load_initial_tables_data(apps, schema_editror):
    DefaultTable = apps.get_model('tables', 'DefaultTable')
    Verb = apps.get_model('verbs', 'Verb')
    tables_name = ['50_verbs', '105_verbs']
    for name in tables_name:
        with open(f'data/{name}.json', 'rb') as file:
            table_data = json.load(file)
        table = DefaultTable(name=name)
        table.save()
        translations = [value['translation'] for value in table_data]
        verbs = Verb.objects.filter(translation__in=translations)
        table.verbs.add(*verbs)


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0001_initial'),
        ('verbs', '0002_add_verbs'),
    ]

    operations = [
        migrations.RunPython(load_initial_tables_data),
    ]
