from rest_framework import serializers

from trades.models import Auction


class AuctionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Auction
        fields = '__all__'
