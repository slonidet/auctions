from rest_framework import serializers

from trades.models import Auction, Bid


class AuctionSerializer(serializers.ModelSerializer):
    current_bid = serializers.ReadOnlyField()

    class Meta:
        model = Auction
        fields = '__all__'
        read_only_fields = ('user',)


class BidSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bid
        fields = '__all__'
