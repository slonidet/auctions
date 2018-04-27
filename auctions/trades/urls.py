from django.conf.urls import url

from . import views


urlpatterns = [
    url('auctions', views.AuctionViewSet.as_view(), name='auctions'),
    url('bids', views.BidViewSet.as_view(), name='bids')
]
