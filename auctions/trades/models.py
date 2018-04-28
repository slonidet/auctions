from django.contrib.auth.models import User
from django.db import models
from django.db.models import Max


class Auction(models.Model):
    """
    Auctions model
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.TextField()
    start_price = models.IntegerField()
    price_step = models.IntegerField()
    finish_time = models.DateTimeField()

    @property
    def current_bid(self):
        aggr = Bid.objects.filter(auction=self.id).aggregate(Max('amount'))
        return aggr['amount__max']

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
