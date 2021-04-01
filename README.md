# CEOS 13기 백엔드 스터디
## REST API 서버 개발
### 인스타그램 클론

## 유의사항
* 본 레포지토리는 백엔드 스터디 2-3주차의 과제를 위한 레포입니다.
* 따라서 해당 레포를 fork 및 clone 후 local에서 본인의 깃헙 ID 브랜치로 작업한 후 커밋/푸시하고, PR 보낼 때도 `본인의 브랜치-> 본인의 브랜치`로 해야 합니다.

## 2주차 과제 (기한: 3/25 목요일까지)
### 모델 설명

* User  
email  
password  
username   
  ...  
  
  
* Profile  
nickname : 닉네임   
  comment  : 간단한 소개  
  user_id  : 회원
  phone_num : 연락처
  website : 웹사이트
  img : 프로필사진  
     

* Post  
text : 글  
  pub_date : 업로드날짜   
  author_id : 글쓴이   
      

* Video  
video : 동영상  
  post_id : 소속게시물    
    
  
* Photo  
image : 사진   
  post_id : 소속게시물 

  
#### media파일
 -FileField 를 통해 저장한 모든 파일을 지칭 (ImageField도 포함)  
-db필드에는 저장경로를 저장  
-실제 파일은 settings.MEDIA_ROOT 경로에 저장  
-모델작성시에 upload_to인자로 더 자세한 저장경로를 지정가
- settings
~~~python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
~~~
- models.py
~~~python
# media/image/ 아래에 저장
photo = models.ImageField(upload_to="image")
# 이미지 업로드 날짜에 따라 디렉토리에 저장 (strftime 으로 포멧팅)
photo = models.ImageField(upload_to="%Y/%m/%d")
~~~
- urls.py
~~~python
# 이미지 url설정
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
~~~



### ORM 적용해보기
* Post 모델 객체넣기 
~~~python
>>> user1 = User(username = 'user1', password = 'abc')
>>> user1.save()
>>> User.objects.all()
<QuerySet [<User: user1>]>
>>> post1 = Post(written = '첫글입니다.', author = user1, pub_date = timezone.now())
>>> post2 = Post(written = '한남동에서 과제중', author = user1, pub_date = timezone.now())
>>> post3 = Post(written = '오늘저녁은 수제버', author = user1, pub_date = timezone.now())
>>> post1.save()
>>> post2.save()
>>> post3.save()
~~~
* 객체 조회 
~~~python
>>> Post.objects.all()
<QuerySet [<Post: 첫글입니다.>, <Post: 한남동에서 과제중>, <Post: 오늘저녁은 수제버거>]>
~~~
* filter함수사용
~~~python
>>> Post.objects.filter(written__startswith='한남동')
<QuerySet [<Post: 한남동에서 과제중>]>
>>> Post.objects.filter(id=3)
<QuerySet [<Post: 오늘저녁은 수제버거>]>
~~~
* relation연습  

##### post의 author조회 
~~~python
>>> post1.author
<User: user1>
>>> post1.author.username
>>> 'user1'
~~~
##### user1의 post 조회하기   
( Post 안에 foreign key 가 있고 그게 User로 향하고 있어서 User은 post_set을 갖는다 )
~~~python
>>> user1 = User.objects.get(id=1)
>>> user1
<User: user1>
>>> user1.post_set.all()
<QuerySet [<Post: 첫글입니다.>, <Post: 한남동에서 과제중>, <Post: 오늘저녁은 수제버거>]>
~~~
* get() 과 filter()차이  

get()은 객체(<User: user1>)를 반환 : 멤버에 접근가능  
  user1.post ( o )  
  
filter()은 queryset(<QuerySet [<User: user1>]>)을 반환 : 멤버접근불가  
user1.post ( x ), user1.username ( x )  
오류 : AttributeError: 'QuerySet' object has no attribute 'username'

  


### 간단한 회고
처음에는 모델링이 생각보다 간단할 줄 알았지만 실제로 하면서 영상과 사진 업로드를 다루는 과정이 생각보다 복잡해서
좀 애를 먹었습니다. 미리보기문제로 마크다운에 추가하진 못했지만 draw.io를 사용해서 모델링을 해보면서 원래는 노트에 하곤 했었는데 너무 편하고
좋았습니다. 앞으로 insta clone을 해서 완성될 모습이 기대가 됩니다.

## 3주차 과제 (기한: 10/3 토요일까지)


### 모델 선택 및 데이터 삽입
선택모델 : Post
~~~python
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
~~~
데이터 조회 
~~~python
>>> Post.objects.all()
<QuerySet [<Post: post: 첫 번째글 by suy2on>, <Post: post: 다시글 by 포슬포슬>, <Post: post: 무야호~ by 포슬포슬>]>
~~~

### 모든 list를 가져오는 API
api/post/ (GET)
~~~python
[
    {
        "id": 1,
        "text": "첫 번째글",
        "like": [
            1
        ],
        "author_nickname": "suy2on"
    },
    {
        "id": 2,
        "text": "다시글",
        "like": [],
        "author_nickname": "포슬포슬"
    },
    {
        "id": 3,
        "text": "무야호~",
        "like": [],
        "author_nickname": "포슬포슬"
    }
]
~~~

### 특정한 데이터를 가져오는 API
api/post/2 (GET)
~~~python
[
    {
        "id": 1,
        "text": "첫 번째글",
        "like": [
            1
        ],
        "author_nickname": "suy2on"
    }
]
~~~


### 새로운 데이터를 create하도록 요청하는 API
요청한 URL 및 Body 데이터의 내용과 create된 결과를 보여주세요!

### (선택) 특정 데이터를 삭제 또는 업데이트하는 API
위의 필수 과제와 마찬가지로 요청 URL 및 결과 데이터를 보여주세요!

### 공부한 내용 정리
새로 알게된 점, 정리 하고 싶은 개념, 궁금한점 등을 정리해 주세요

### 간단한 회고
과제 시 어려웠던 점이나 느낀 점, 좋았던 점 등을 간단히 적어주세요!