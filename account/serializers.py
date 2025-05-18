from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            nickname = validated_data['nickname'],
            name = validated_data['name'],
            password = validated_data['password']
        )
        return user
    class Meta:
        model = User
        fields = ['nickname', 'email', 'name', 'password']
    
from .models import Blog
from rest_framework import serializers

class BlogSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.nickname')
    class Meta:
        model = Blog
        fields =  ['id', 'title', 'create_at', 'user', 'body']

class PostImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = PostImage
        fields = ['image']


class PostSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

	#게시글에 등록된 이미지들 가지고 오기
    def get_images(self, obj):
        image = obj.image.all() 
        return PostImageSerializer(instance=image, many=True, context=self.context).data

    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        instance = Post.objects.create(**validated_data)
        image_set = self.context['request'].FILES
        for image_data in image_set.getlist('image'):
            PostImage.objects.create(post=instance, image=image_data)
        return instance
