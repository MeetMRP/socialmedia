from rest_framework import serializers
from .models import Post, Like, Connection
from accounts.models import User

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'content', 'related_url', 'author')
        extra_kwargs = {'author': {'read_only': True}}

    def create(self, validated_data):
        post = Post.objects.create(
            content = validated_data['content'], 
            related_url = validated_data['related_url'], 
            author = validated_data['author'], 
        )
        return post
    

class SentConnectSerializer(serializers.ModelSerializer):
    addressee_username = serializers.CharField(write_only=True)

    class Meta:
        model = Connection
        fields = ('id', 'requester', 'addressee', 'status', 'addressee_username')
        extra_kwargs = {
            'requester': {'read_only': True}, 
            'addressee': {'read_only': True}, 
            'status': {'read_only': True}
        }


    def validate_addressee_username(self, value):
        try:
            user = User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this username does not exist.")
        return user

    def create(self, validated_data):
        addressee = validated_data.pop('addressee_username', None)
        if Connection.objects.filter(requester=validated_data['requester'], addressee=addressee).exists():
            raise serializers.ValidationError('Request already sent')
        
        connection = Connection.objects.create(
            requester=validated_data['requester'],
            addressee=addressee,
            status=validated_data.get('status', 'pending')
        )
        return connection
    
class GetConnectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = '__all__'

class UpdateConnectStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = ['status']
        extra_kwargs = {
            'requester': {'read_only': True}, 
            'addressee': {'read_only': True}, 
            'creation_date': {'read_only': True}
        }