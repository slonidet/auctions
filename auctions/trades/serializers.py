from rest_framework import serializers

from trades.models import Auction, Bid


class AuctionSerializer(serializers.ModelSerializer):
    current_bid = serializers.ReadOnlyField()
    is_active = serializers.ReadOnlyField()

    class Meta:
        model = Auction
        fields = '__all__'
        read_only_fields = ('user', 'winner')


class AuctionRetrieveSerializer(serializers.ModelSerializer):
    bids = serializers.SerializerMethodField()

    class Meta:
        model = Auction
        fields = ('user', 'id', 'bids')
        read_only_fields = ('user',)

    def get_bids(self, obj):
        bids = Bid.objects.filter(auction=obj).values(
            'amount', 'user__first_name', 'user__last_name')
        return bids


class BidSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bid
        fields = '__all__'
        read_only_fields = ('user',)

    def validate(self, attrs):
        """
        Check if bid's amount meets auction's price step and bigger than
        current bid amount
        """
        auction = attrs.get('auction')
        message = 'The bid must be at least ${st} more than ${am}'.format(
            st=auction.price_step, am=auction.current_bid)

        if attrs.get('amount') % auction.price_step:
            raise serializers.ValidationError(message)

        if attrs.get('amount') <= auction.current_bid:
            raise serializers.ValidationError(message)

        return attrs
