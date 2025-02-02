from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "is_staff",
        )
        read_only_fields = ("id", "is_staff")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """create and return a new `User`
        instance, given the validated data."""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """update and return an `User` instance, given the validated data."""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
