from rest_framework import serializers
import re   # 정규식 쓰기위한 모듈
from api.models import *



class VideoSerializer(serializers.ModelSerializer):
    post_author = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = '__all__'

    def get_post_author(self, obj): # video 객체
        return obj.post.author

class PhotoSerializer(serializers.ModelSerializer):
    post_author = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = '__all__'

    def get_post_author(self, obj): # photo 객체
        return obj.post.author

class PostSerializer(serializers.ModelSerializer):
    author_nickname = serializers.SerializerMethodField() # post_user라는 field추가 그 값은 get_post_user의 return값
    photos = PhotoSerializer(many=True, read_only=True)
    videos = VideoSerializer(many=True, read_only=True)
    class Meta:
        model = Post  # 사용할 모델
        fields = ['id', 'text', 'like', 'author_nickname', 'author', 'photos', 'videos']

    def get_author_nickname(self, obj): # obj는 Post객
        return obj.author.nickname



class ProfileSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)
    user_password = serializers.SerializerMethodField()
    user_username = serializers.SerializerMethodField()

    class Meta:
        model = Profile  # 사용할 모델
        fields = '__all__'


    def get_user_password(self, obj):
            return obj.user.password

    def get_user_username(self, obj):
        return obj.user.username

    def validate_phone_num(self, value):
        pattern = '\d{3}-\d{4}-\d{4}'
        phoneReg = re.compile(pattern)
        print(value)
        if(phoneReg.match(value) == None):
            raise serializers.ValidationError("핸드폰번호는 xxx-xxxx-xxxx 형식이어야합니다.")
        return value

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
