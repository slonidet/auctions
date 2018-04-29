from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from auctions.celery import app
from trades.models import Auction, Bid


@app.task(name='notificate_expired_auction')
def notificate_expired_auction():
    auctions = Auction.objects.all()
    for auction in auctions:
        users = User.objects.filter(auctions=auction)
        winner_bid = Bid.objects.get(
            auction=auction, amount=auction.current_bid)
        winner = winner_bid.user

        title = 'Auction {ttl} just expired'.format(ttl=auction.title)
        body = 'Auction {ttl} just expired. {usr} won'.format(
            ttl=auction.title, usr=winner
        )
        users = users.exclude(winner)
        email = EmailMessage(title, body, to=[user.email for user in users])
        if not (auctions.is_active and auction.exp_email_sent):
            email.send()
            auction.exp_email_sent = True
            auction.save()
