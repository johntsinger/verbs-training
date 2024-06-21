from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from tables.models import Table
from results.models import Result


@receiver(
    m2m_changed,
    sender=Table.verbs.through,
    dispatch_uid="table_changed"
)
def delete_results(sender, instance, action, pk_set, **kwargs):
    """Delete results if verb is deleted from table"""
    if action == 'pre_remove':
        Result.objects.filter(verb_id__in=pk_set, table=instance).delete()
