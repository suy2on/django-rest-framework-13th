from django.db import models
from django.contrib.auth.models import User


# User 와 1대1 관계
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=10, unique=True)
    comment = models.TextField(max_length= 200, null= True, blank=True)
    web_site = models.TextField(max_length= 100, null= True, blank=True)
    phone_num = models.TextField(max_length= 15)
    img = models.ImageField(upload_to="profile_img", null= True, blank=True)

    def __str__(self):
        return self.nickname


# User 와 1대다 관계
class Post(models.Model):
    text = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name= 'posts')
    pub_date = models.DateTimeField(auto_now_add = True)
    like = models.ManyToManyField(Profile, related_name='like_posts', blank=True, null=True)
    def __str__(self):
        return 'post: {} by {}'.format(self.text, self.author.nickname)

    def like_count(self):
        return self.like.count()

class Photo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name= 'photos')
    image = models.ImageField(upload_to="image")  # media/image에 이미지들 저장

    def __str__(self):
        return self.post.text

class Video(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name= 'videos')
    video = models.FileField(upload_to="video")  # media/video에 영상들 저장

    def __str__(self):
        return self.post.text


