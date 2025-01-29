from rest_framework import serializers
from django.contrib.auth.models import User
from auth_app.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)  # Prevent password exposure


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Keep user read-only

    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'phone', 'address', 'organization',
            'adharcard', 'is_farmer', 'acre_of_land', 'kisan_card',
            'is_buyer', 'gst'
        ]
        extra_kwargs = {
            'adharcard': {'required': False, 'allow_null': True}
        }

    def create(self, validated_data):
        user_data = self.context.get('user_data', {})

        # Ensure mandatory fields exist
        if not user_data.get('username') or not user_data.get('password') or not user_data.get('email'):
            raise serializers.ValidationError(
                {"user": "Missing required user fields"})

        # Check if user already exists
        if User.objects.filter(username=user_data['username']).exists():
            raise serializers.ValidationError(
                {"user": "Username already exists"})

        # Create the User first
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password']
        )

        # Assign the user to UserProfile and save
        user_profile = UserProfile.objects.create(user=user, **validated_data)
        return user_profile
