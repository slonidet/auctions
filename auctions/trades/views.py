from django.http import HttpResponseForbidden
from rest_framework import mixins, generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSetMixin, ModelViewSet

from trades import serializers
from trades.models import Auction, Bid
from trades.serializers import AuctionSerializer, BidSerializer


class AuctionViewSet(ModelViewSet):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.AuctionRetrieveSerializer
        return super().get_serializer_class()


class BidViewSet(generics.CreateAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        auction = serializer.validated_data.get('auction')
        owner = auction.user
        user = self.request.user
        if owner.id == user.id:
            raise PermissionDenied(
                "You can't do bids since you're auction's owner")
        serializer.save(user=user)
