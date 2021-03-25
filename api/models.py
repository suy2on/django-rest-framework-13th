from django.db import models
from django.contrib.auth.models import User
import datetime

# User 와 1대1 관계
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=10)
    comment = models.TextField(max_length= 200)

# User 와 1대다 관계
class Post(models.Model):
    written = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE) # 로그인된 user
    pub_date = models.DateTimeField('date published', default=datetime.datetime.now, editable=False)

    def __str__(self):
        return self.written

class Photo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="image")  # media/image에 이미지들 저장

    def __str__(self):
        return self.post.written

class Video(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    video = models.FileField(upload_to="video")  # media/video에 영상들 저장

    def __str__(self):
        return self.post.written
