from django.contrib.auth.models import User
from django.db import models


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

    def __str__(self):
        return self.title
