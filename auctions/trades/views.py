from rest_framework import mixins, generics
from rest_framework.authentication import TokenAuthentication, \
    SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from trades.models import Auction, Bid
from trades.serializers import AuctionSerializer, BidSerializer


class AuctionViewSet(mixins.RetrieveModelMixin, generics.ListCreateAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BidViewSet(generics.CreateAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
