from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from profiles.models import Profile
from tables.models import DefaultTable, UserTable


User = get_user_model()


@receiver(
    post_save,
    sender=User,
    dispatch_uid='create_user_profile'
)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(
    post_save,
    sender=User,
    dispatch_uid='save_user_profile'
)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(
    post_save,
    sender=Profile,
    dispatch_uid='create_and_save_user_default_tables'
)
def create_and_save_user_default_table(sender, instance, created, **kwargs):
    if created:
        default_tables = DefaultTable.objects.prefetch_related('verbs')
        for default_table in default_tables:
            table = UserTable.objects.create(
                name=default_table.name,
                profile=instance,
            )
            table.verbs.set(
                default_table.verbs.all()
            )
