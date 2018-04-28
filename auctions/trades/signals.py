from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver

from trades.models import Auction


@receiver(post_save, sender=Auction)
def auction_mail(sender, instance, created, **kwargs):
    """
    Send notifications about new auction
    """
    if created:
        title = 'New auction is avalable'
        body = 'You can take a part in this auction: {title}'.format(
            title=instance.title
        )
        users = User.objects.all()
        email = EmailMessage(title, body, to=[user.email for user in users])
        email.send()
