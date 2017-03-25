from rest_framework import serializers

from apps.authentication.models import OnlineUser as User


class PublicUserSerializer(serializers.ModelSerializer):
    """
    Serializer for publicly available user endpoint
    """
    rfid = serializers.HiddenField(default='')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'rfid',)
