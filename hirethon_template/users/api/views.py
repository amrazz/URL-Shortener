from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from hirethon_template.organizations.services import OrganizationService

from .serializers import UserLoginSerializer, UserRegisterSerializer

User = get_user_model()


class UserRegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        organization = OrganizationService.create_organization_with_admin(user)
        refresh = RefreshToken.for_user(user)

        response_data = {
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name or user.email,
            },
            "organization": {
                "id": organization.id,
                "name": organization.name,
            },
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            "message": "User registered successfully",
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


class UserLoginAPIView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        response_data = {
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name or user.email,
            },
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            "message": "Login successful",
        }

        return Response(response_data, status=status.HTTP_200_OK)
