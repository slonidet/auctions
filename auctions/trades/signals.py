from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver

from trades.models import Auction, Bid


@receiver(post_save, sender=Auction)
def auction_creation_mail(sender, instance, created, **kwargs):
    """
    Send notifications about creating new auction
    """
    if created:
        title = 'New auction is avalable'
        body = 'You can take a part in this auction: {title}'.format(
            title=instance.title
        )
        users = User.objects.filter(is_active=True).exclude(auction=instance)
        email = EmailMessage(title, body, to=[user.email for user in users])
        email.send()


@receiver(post_save, sender=Bid)
def auction_notifications_mail(sender, instance, created, **kwargs):
    """
    Send notifications about the auction
    """
    if created:
        auction = Auction.objects.get(bid=instance)
        users = User.objects.filter(
            is_active=True, auction=auction).exclude(bid=instance)
        title = "The price on {ttl} was changed".format(ttl=auction.title)
        body = "The price on {ttl} was changed to {am}".format(
            ttl=auction.title, am=instance.amount)
        email = EmailMessage(title, body, to=[user.email for user in users])
        email.send()
