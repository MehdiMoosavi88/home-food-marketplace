from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.accounts.models import User
from apps.cooks.models import CookProfile
from apps.menus.models import Menu


@receiver(post_save, sender=User)
def create_cook_profile(sender, instance, created, **kwargs):

    if not created:
        return

    if instance.role != User.Roles.COOK:
        return

    cook_profile, _ = CookProfile.objects.get_or_create(
        user=instance,
        defaults={
            "phone": "",
            "city": "",
            "address": "",
        }
    )

    Menu.objects.get_or_create(
        cook=cook_profile,
        defaults={
            "title": f"{instance.username}'s Menu"
        }
    )