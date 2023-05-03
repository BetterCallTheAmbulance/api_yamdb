from rest_framework import serializers, status

from django.core.validators import RegexValidator

from rest_framework.response import Response

from reviews.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate(self, data):
        if (data.get('username') is not None
                and data.get('username').lower() == 'me'):
            raise serializers.ValidationError(
                'Username должен иметь отличное значение от "me"'
            )
        return data


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[
        RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Неккоректно введён <username>',
            code='invalid_username'
        )
    ],
        max_length=150
    )

    def validate_username(self, value):
        if value is None:
            return Response({'username': 'Username is required.'},
                            status=status.HTTP_400_BAD_REQUEST)
        elif value.lower() == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать Юзернейм - "me"'
                )
        return value

    class Meta:
        model = User
        fields = ('email', 'username')


class JWTTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=50)
