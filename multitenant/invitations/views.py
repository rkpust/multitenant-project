from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Invitation
from .serializers import LoginSerializer, InvitationSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
import json
from django.contrib.auth.models import User
from decouple import config
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.
class LoginView(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            username = serializer.data['username']
            password = serializer.data['password']

            user = authenticate(username=username, password=password)

            if user is None:
                return Response({
                'status': 400,
                'message': 'Username or Password is wrong',
                'data': {}
            })

            refresh = RefreshToken.for_user(user)

            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            })
        else:
            return Response({
                'status': 400,
                'message': 'Something is went wrong',
                'data': serializer.error
            })

# Invitation
class InvitationCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = InvitationSerializer(data=request.data)
        if serializer.is_valid():
            invitation = serializer.save()
            invitation.set_expiration()
            invitation.save()
            
            # Send the email (implement send_email function as needed)
            self.send_invitation_email(invitation)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_client_ip(self, request):
        ip = request.META.get('HTTP_X_FORWARDED_FOR').split(',')[0] if request.META.get('HTTP_X_FORWARDED_FOR') else request.META.get('REMOTE_ADDR')
        user_agent = request.headers.get('User-Agent')
        return ip, user_agent

    def send_invitation_email(self, invitation):
        ip_address, user_agent = self.get_client_ip(self.request)
        invitation.metadata = json.dumps({'ip': ip_address, 'user_agent': user_agent})
        invitation.save()

        # Send the email logic here
        subject = 'Invitation for a multi-tenant platform'

        message = f'A invitation link is created for {invitation.tenant.name}\n Link: {invitation.tenant.domain}/accept/{invitation.token}'
        from_email = settings.DEFAULT_FROM_EMAIL  # Default email address from settings
        recipient_list = [invitation.email]  # List of recipients

        # Send email
        send_mail(subject, message, from_email, recipient_list)



# Accept Invitation
class InvitationAcceptAPIView(APIView):
    def post(self, request, token, *args, **kwargs):
        try:
            invitation = Invitation.objects.get(token=token, status='PENDING')
        except Invitation.DoesNotExist:
            return Response({'error': 'Invalid token or invitation expired'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Here, you would set the password (ensure you validate the password field)
        password = request.data.get('password')
        if password:
            user = User.objects.create_user(username=invitation.email, password=password)
            invitation.status = 'ACCEPTED'
            invitation.save()
            return Response({'message': 'Invitation accepted successfully.'}, status=status.HTTP_200_OK)
        return Response({'error': 'Password required.'}, status=status.HTTP_400_BAD_REQUEST)


# Cancel Invitation
class InvitationCancelAPIView(APIView):
    def post(self, request, token, *args, **kwargs):
        try:
            invitation = Invitation.objects.get(token=token, status='PENDING')
        except Invitation.DoesNotExist:
            return Response({'error': 'Invalid token or invitation expired'}, status=status.HTTP_400_BAD_REQUEST)
        
        invitation.status = 'CANCELLED'
        invitation.save()
        
        return Response({'message': 'Invitation cancelled.'}, status=status.HTTP_200_OK)
