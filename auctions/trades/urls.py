from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from trades.views import AuctionViewSet
from . import views


router = DefaultRouter()
router.register(r'auctions', AuctionViewSet, base_name='auctions')

urlpatterns = [
    url('bids', views.BidViewSet.as_view(), name='bids')
] + router.urls
