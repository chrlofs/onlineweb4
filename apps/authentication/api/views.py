from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope
from rest_framework import permissions, viewsets

from apps.authentication.models import OnlineUser as User
from apps.authentication.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    Viewset for private User serializer.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
