from django.contrib.auth.models import User
from django.db import models
from django.db.models import Max
from django.utils import timezone


class Auction(models.Model):
    """
    Auctions model
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='auction')
    winner = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='won_auction',
        blank=True, null=True)
    title = models.CharField(max_length=250)
    description = models.TextField()
    start_price = models.IntegerField()
    price_step = models.IntegerField()
    finish_time = models.DateTimeField()
    exp_email_sent = models.BooleanField(
        help_text='shows if expiration email was sent on this auction',
        default=False
    )

    @property
    def current_bid(self):
        aggr = Bid.objects.filter(auction=self.id).aggregate(Max('amount'))
        if not aggr['amount__max']:
            return 0
        return aggr['amount__max']

    @property
    def is_active(self):
        return self.finish_time > timezone.now()

    def __str__(self):
        return self.title


class Bid(models.Model):
    """
    Bid model
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return '{user}, {auction}, {amount}'.format(
            user=self.user, auction=self.auction, amount=self.amount)
