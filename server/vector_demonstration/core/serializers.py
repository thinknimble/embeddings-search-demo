from django.contrib.auth import login
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import JobDescription, JobDescriptionChunk, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "full_name",
        )


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(allow_blank=False, required=True)
    password = serializers.CharField(allow_blank=False, required=True)

    class Meta:
        model = User
        fields = (
            "email",
            "password",
        )

    def validate_email(self, value):
        """Emails are always stored and compared in lowercase."""
        return value.lower()

    @staticmethod
    def login(user, request):
        """
        Log-in user and append authentication token to serialized response.
        """
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        auth_token, token_created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(user, context={"request": request})
        response_data = serializer.data
        response_data["token"] = auth_token.key
        return response_data


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "password",
        )
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate(self, data):
        password = data.get("password")
        validate_password(password)

        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class JobDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDescription
        fields = (
            "id",
            "title",
            "company",
            "location",
            "description",
            "skills",
            "language",
        )


class JobDescriptionChunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDescriptionChunk
        fields = (
            "job_description_id",
            "chunk",
            "token_count",
            "embedding",
        )


class JobDescriptionQuerySerializer(serializers.Serializer):
    query = serializers.CharField(required=True)


class JobDescriptionSearchResultsSerializer(serializers.Serializer):
    score = serializers.FloatField(required=True)
    job_description = JobDescriptionSerializer(required=True)
    chunks = JobDescriptionChunkSerializer(required=True, many=True)
