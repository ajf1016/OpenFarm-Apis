from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from auth_app.serializers import UserProfileSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import UserProfile


@api_view(['POST'])
@permission_classes([AllowAny])
def create_user_with_profile(request):
    user_data = {
        "username": request.data.get('username'),
        "email": request.data.get('email'),
        "password": request.data.get('password'),
    }

    profile_data = {
        "phone": request.data.get('phone'),
        "is_farmer": request.data.get('is_farmer', False),
    }

    # Required fields validation
    required_user_fields = ["username", "email", "password"]
    missing_user_fields = [
        field for field in required_user_fields if not user_data[field]]

    required_profile_fields = ["phone"]
    missing_profile_fields = [
        field for field in required_profile_fields if not profile_data[field]]

    if missing_user_fields or missing_profile_fields:
        return Response({
            "status_code": 6001,
            "message": "Missing required fields",
            "missing_fields": missing_user_fields + missing_profile_fields
        }, status=400)

    # Serializers
    user_serializer = UserSerializer(data=user_data)
    if user_serializer.is_valid():
        profile_serializer = UserProfileSerializer(
            data=profile_data, context={'user_data': user_data})

        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response({"status_code": 6000, "message": "User created successfully"}, status=201)
        else:
            return Response({
                "status_code": 6001,
                "message": "Invalid profile data",
                "profile_errors": profile_serializer.errors
            }, status=400)
    else:
        return Response({
            "status_code": 6001,
            "message": "Invalid user data",
            "user_errors": user_serializer.errors
        }, status=400)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    phone = request.data.get('phone')
    password = request.data.get('password')

    if phone is None or password is None:
        return Response({
            "status_code": 6001,
            "message": "Please provide both phone number and password"
        }, status=400)

    try:
        user_profile = UserProfile.objects.get(phone=phone)
        user = user_profile.user  # Get the associated User object
    except UserProfile.DoesNotExist:
        return Response({
            "status_code": 6001,
            "message": "Invalid phone number or password"
        }, status=400)

    # Authenticate using the user's username and provided password
    user = authenticate(username=user.username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            "status_code": 6000,
            "message": "Login successful",
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "is_farmer": user_profile.is_farmer,
            "is_buyer": user_profile.is_buyer,
            "phone": user_profile.phone,
            "name": user.username,
            "user_id": user.id
        }, status=200)
    else:
        return Response({
            "status_code": 6001,
            "message": "Invalid phone number or password"
        }, status=400)
