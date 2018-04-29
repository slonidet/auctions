from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def api_root(request, format=None):
    params = {'request': request, 'format': format}
    links = {
        'user:authentication': reverse('login', **params),
        'user:registration': reverse('user-registrate', **params),
        'auctions': reverse('auctions-list', **params),
        'bids': reverse('bids', **params)
    }
    return Response(links)
