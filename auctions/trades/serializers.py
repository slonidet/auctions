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
        read_only_fields = ('user',)

    def validate(self, attrs):
        """
        Check if bid's amount meets auction's price step and bigger than
        current bid amount
        """
        auction = attrs.get('auction')

        if attrs.get('amount') % auction.price_step:
            raise serializers.ValidationError(
                'Your bid must be at least $ {step} more than current '
                'bid ($ {amount})'.format(step=auction.price_step,
                                          amount=auction.current_bid))
        # if attrs.get('amount') <= auction.current_bid:
        #     raise serializers.ValidationError(
        #         'Your bid must be bigger than current bid ($ {amount)'.format(
        #             amount=auction.current_bid
        #         )
        #     )
        return attrs
