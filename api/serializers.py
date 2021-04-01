from rest_framework import serializers
from api.models import Post, Profile


class PostSerializer(serializers.ModelSerializer):
    author_nickname = serializers.SerializerMethodField() # post_user라는 field추가 그 값은 get_post_user의 return값

    class Meta:
        model = Post  # 사용할 모델
        fields = ['id', 'text', 'like', 'author_nickname', 'author']

    def get_author_nickname(self, obj): # obj는 Post객
        return obj.author.nickname



class ProfileSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Profile  # 사용할 모델
        fields = ['id', 'nickname', 'web_site', 'phone_num', 'posts', 'comment', 'img']