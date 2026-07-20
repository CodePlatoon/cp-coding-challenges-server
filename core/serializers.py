from rest_framework import serializers
from .models import User, CodingChallenge, SelectedChallenge


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user


class CodingChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodingChallenge
        fields = ('id', 'mini_lesson', 'init_temp', 'order')
        # NOTE: 'tests' is intentionally excluded — never sent to client


class SelectedChallengeSerializer(serializers.ModelSerializer):
    challenge = CodingChallengeSerializer(read_only=True)

    class Meta:
        model = SelectedChallenge
        fields = ('id', 'challenge', 'submission', 'passed')
