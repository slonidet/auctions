from rest_framework.viewsets import ReadOnlyModelViewSet

from trades.models import Auction
from trades.serializers import AuctionSerializer


class AuctionViewSet(ReadOnlyModelViewSet):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
