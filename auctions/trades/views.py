from django.utils import timezone
from rest_framework import mixins, generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from trades import serializers
from trades.models import Auction, Bid
from trades.serializers import AuctionSerializer, BidSerializer


class AuctionViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.AuctionRetrieveSerializer
        return super().get_serializer_class()

    def filter_active(self, qs):
        return qs.filter(finish_time__gte=timezone.now())

    def filter_inactive(self, qs):
        return qs.filter(finish_time__lt=timezone.now())

    def get_queryset(self):
        qs = super(AuctionViewSet, self).get_queryset()
        is_active = self.request.GET.get('is_active', None)
        if is_active is None:
            pass
        elif is_active == 'true':
            qs = self.filter_active(qs)
        elif is_active == 'false':
            qs = self.filter_inactive(qs)
        else:
            pass
        return qs


class BidAPIView(generics.CreateAPIView):
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
        if not auction.is_active:
            raise PermissionDenied(
                "This auction is expired"
            )
        serializer.save(user=user)
