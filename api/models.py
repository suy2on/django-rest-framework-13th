from django.db import models
from django.contrib.auth.models import User
import datetime

# User 와 1대1 관계
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=10)
    comment = models.TextField(max_length= 200, null= True, blank=True)
    website = models.TextField(max_length= 100, null= True, blank=True)
    phone_num = models.TextField(max_length= 15)
    img = models.ImageField(upload_to="profile_img", null= True, blank=True)

    def __str__(self):
        return self.nickname


# User 와 1대다 관계
class Post(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published', default=datetime.datetime.now, editable=False)

    def __str__(self):
        return 'post: {} by {}'.format(self.text, self.author.profile.nickname)

class Photo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="image")  # media/image에 이미지들 저장

    def __str__(self):
        return self.post.text

class Video(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    video = models.FileField(upload_to="video")  # media/video에 영상들 저장

    def __str__(self):
        return self.post.text
