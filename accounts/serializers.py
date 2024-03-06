from rest_framework import serializers
from django.contrib.auth import authenticate
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'f_name', 'l_name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create(
            username = validated_data['username'], 
            email = validated_data['email'], 
            f_name = validated_data['f_name'], 
            l_name = validated_data['l_name'], 
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError({'message': 'Invalid credentials'})
    
    
class UserPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['f_name', 'l_name','profile_picture', 'bio']