from django.db import transaction
from django.db.models.signals import m2m_changed, post_save, post_delete
from django.dispatch import receiver
from tables.models import DefaultTable, UserTable


@receiver(
    m2m_changed,
    sender=DefaultTable.verbs.through,
    dispatch_uid="default_table_verbs_changed"
)
def update_user_table(sender, instance, **kwargs):
    """
    Set UserTable.verbs m2m if a new DefaultTable is created or
    if DefaultTable.verbs m2m is updated.
    """

    # signals send are add and clear --> set(clear=True) clear m2m and add
    with transaction.atomic():
        for table in UserTable.objects.filter(name=instance.name):
            table.verbs.set(
                instance.verbs.all(),
                clear=True
            )


@receiver(
    post_delete,
    sender=DefaultTable,
    dispatch_uid="default_table_deleted"
)
def delete_user_table(sender, instance, **kwargs):
    """
    Delete UserTable objects if related DefaultTable is deleted.
    """
    UserTable.objects.filter(name=instance.name).delete()
