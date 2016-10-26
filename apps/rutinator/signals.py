from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Task
from .send_mail import send_email


@receiver(post_save, sender=Task)
def new_membership_approval_handler(sender, instance, created, **kwargs):
    """

    :param sender: The sending model.
    :type sender: MembershipApproval
    :param instance: The MembershipApproval instance
    :type instance: MembershipApproval
    :param created: True or False, whether this instance is new or not.
    :type created: bool
    :param kwargs: Other parameters.
    :type kwargs: dict
    :return: Nothing
    :rtype: None
    """

    if created:
        if settings.APPROVAL_SETTINGS.get('SEND_APPROVER_NOTIFICATION_EMAIL', False):
            send_email(instance)
