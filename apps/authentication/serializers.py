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


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for authenticated access to own user profile
    """
    class Meta:
        model = User
        fields = ('field_of_study', 'started_date', 'compiled', 'infomail', 'jobmail', 'online_mail',
                  'phone_number', 'address', 'zip_code', 'allergies', 'mark_rules', 'rfid', 'nickname', 'username',
                  'website', 'github', 'linkedin', 'gender', 'bio', 'ntnu_username',)
        read_only_fields = ('field_of_study', 'started_date', 'compiled', 'online_mail', 'rfid', 'username',
                            'website', 'github', 'linkedin', 'gender', 'bio',)
