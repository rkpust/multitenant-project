from rest_framework import serializers
from .models import Invitation

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        # fields = ['id', 'tenant', 'name', 'email', 'status', 'token', 'expiration_date', 'metadata']
        fields = ['id', 'tenant', 'name', 'email', 'status', 'token', 'metadata']
