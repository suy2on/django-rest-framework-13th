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
api/posts (GET)
~~~python
GET /api/posts
HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

[
    {
        "id": 1,
        "text": "첫 번째글",
        "like": [
            1
        ],
        "author_nickname": "suy2on",
        "author": 2,
        "photos": [],
        "videos": []
    },
    {
        "id": 2,
        "text": "다시글",
        "like": [],
        "author_nickname": "포슬포슬",
        "author": 1,
        "photos": [],
        "videos": []
    },
    {
        "id": 3,
        "text": "무야호~",
        "like": [],
        "author_nickname": "포슬포슬",
        "author": 1,
        "photos": [],
        "videos": []
    },
    {
        "id": 4,
        "text": "post 이용해서 넣는 문장",
        "like": [],
        "author_nickname": "포슬포슬",
        "author": 1,
        "photos": [],
        "videos": []
    },
    {
        "id": 5,
        "text": "post 이용해서 넣는 두번째 문장",
        "like": [],
        "author_nickname": "포슬포슬",
        "author": 1,
        "photos": [],
        "videos": []
    }
]
~~~

### 특정한 데이터를 가져오는 API
api/users/2/posts (GET)
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
api/posts (POST)
{ "text": "post 이용해서 넣는 두번째 문장",
 "author" : 1 
}
~~~python
{
    "id": 5,
    "text": "post 이용해서 넣는 두번째 문장",
    "like": [],
    "author_nickname": "포슬포슬",
    "author": 1
}
~~~


### 공부한 내용 정리
* #### serializer에 field 넣어야하는 것
  - fields = __all__, exclude, 직접 명시 ('id', 'name') 과 같은 방식들로 넣을 수 있음  
  - forignkey로 연결된 field는 넣어주어야 한다 ( 아직 정확한 이유는 찾지 못했습니다 ㅠㅠ )
  - 기존에 있던 field가 아닌 걸 추가하고 싶다면 : serializer.SerializerMethodField()로 정의해준뒤  
   get_<field_name> 이름의 메소드를 만들어주면 된다  
  - serializers.StringRelatedField() 를 사용해주면 ForgeignKey로 연결된 모델의 __str__ 메소드에서 정의한 string를 리턴  
  - 1:n 에서 1쪽의 serializer에서 n을 위한 변수를 만들었다면 (PostSerializer의 photos같이)
  꼭 field에 넣어줘야한다  
    (에러: AssertionError: The field 'photos' was declared on serializer PostSerializer, but has not been included in the 'fields' option.
)
* #### REST API 작성요령
  - GET 전체조회, POST 같은 경우에는 id값을 붙여주지 않는다  
  - resource부분에 명사는 복수형으로 쓴다 (api/posts)
  - resource와 따라오는 id가 연관되게 쓴다 ( api/posts/2 -> api/users/2/posts )
  - 소문자로 작성한다
  - 마지막에는 /를 추가하지 않는다
  - _를 사용하지 않는 (대신 하이픈(-)을 사용해준다)
  
* #### FK(foreignKey) field data 넘겨주기
  post의 author(작성자)를 넘겨줄 때 { 'author' : 객체 -> id }로 넘져준다  
  db에서 id값만 가져와서 저장하고 있기때문이다 (author_id)


### 간단한 회고
평소에 rest-api를 이론으로만 봤을 때는 어렵지 않다고 생각하고 있었는데 막상 이렇게 제대로 짜보려니 생각해야할 것들이 
꽤 많다고 느꼈습니다. 그래도 이전에 프로젝트에서는 url이 너무 많아지거나 일정한 규칙없이 늘어나서 가독성도 떨어지고 
관리에 어려움을 겪었는데 이렇게 rest-api를 배우고 나니 그런부분들이 많이 개선될 수 있을것같아서 좋았습니다. 또 serializer
를 배우기 전에는 jsonify로 많이 응답을 보내곤 했었는데요 이렇게 뭔가 json형식으로 만들어주는 방법을 배워서 기쁘고 제네릭처럼
조금 생소하고 어려웠지만 유용하게 쓸 수 있을거같다는 생각이 들었습니다! 물론 아직 완전 기초적인 부분들만 한것 같아서 
앞으로 더 rest-api에대해 알아가는 시간들을 가졌으면 좋겠고 많이 배워야겠다는 생각이 듭니다!!


## 4주차 과제 (기한: 4/8 목요일까지)
### 모든 list를 가져오는 API
GET api/contents/
~~~python
[
    {
        "id": 1,
        "text": "첫 번째글",
        "like": [
            1
        ],
        "author_nickname": "suy2on",
        "author": 2,
        "photos": [],
        "videos": []
    },
    {
        "id": 2,
        "text": "다시글",
        "like": [],
        "author_nickname": "포슬포슬",
        "author": 1,
        "photos": [],
        "videos": []
    },
    {
        "id": 3,
        "text": "무야호~",
        "like": [],
        "author_nickname": "포슬포슬",
        "author": 1,
        "photos": [],
        "videos": []
    },
    {
        "id": 4,
        "text": "post 이용해서 넣는 문장",
        "like": [],
        "author_nickname": "포슬포슬",
        "author": 1,
        "photos": [],
        "videos": []
    },
    {
        "id": 5,
        "text": "post 이용해서 넣는 두번째 문장",
        "like": [],
        "author_nickname": "포슬포슬",
        "author": 1,
        "photos": [],
        "videos": []
    },
    {
        "id": 6,
        "text": "또 다른 시도",
        "like": [],
        "author_nickname": "suy2on",
        "author": 2,
        "photos": [],
        "videos": []
    }
]
~~~


### 특정 데이터를 가져오는 API
GET api/contents/2
~~~python
{
    "id": 2,
    "text": "다시글",
    "like": [],
    "author_nickname": "포슬포슬",
    "author": 1,
    "photos": [],
    "videos": []
}
~~~

### 새로운 데이터를 생성하는 API
POST api/contents/ { "text" : "중간고사전 마지막 과제하는 중", "author" : 1 }
~~~python
{
    "id": 7,
    "text": "중간고사전 마지막 과제하는 중",
    "like": [],
    "author_nickname": "포슬포슬",
    "author": 1,
    "photos": [],
    "videos": []
}
~~~

### 특정 데이터를 업데이트하는 API
PUT api/contents/2 { "text" : "text 수정합니다" , "author" :  1 }
~~~python
{
    "id": 2,
    "text": "text 수정합니다",
    "like": [],
    "author_nickname": "포슬포슬",
    "author": 1,
    "photos": [],
    "videos": []
}
~~~

### 특정 데이터를 삭제하는 API
DELETE api/contents/2  
"DELETE /api/contents/2 HTTP/1.1" 204 0
~~~python
[
    {
        "id": 1,
        "text": "첫 번째글",
        "like": [
            1
        ],
        "author_nickname": "suy2on",
        "author": 2,
        "photos": [],
        "videos": []
    },
    {
        "id": 3,
        "text": "무야호~",
        "like": [],
        "author_nickname": "포슬포슬",
        "author": 1,
        "photos": [],
        "videos": []
    },
    {
        "id": 4,
        "text": "post 이용해서 넣는 문장",
        "like": [],
        "author_nickname": "포슬포슬",
        "author": 1,
        "photos": [],
        "videos": []
    },
    {
        "id": 5,
        "text": "post 이용해서 넣는 두번째 문장",
        "like": [],
        "author_nickname": "포슬포슬",
        "author": 1,
        "photos": [],
        "videos": []
    },
    {
        "id": 6,
        "text": "또 다른 시도",
        "like": [],
        "author_nickname": "suy2on",
        "author": 2,
        "photos": [],
        "videos": []
    },
    {
        "id": 7,
        "text": "중간고사전 마지막 과제하는 중",
        "like": [],
        "author_nickname": "포슬포슬",
        "author": 1,
        "photos": [],
        "videos": []
    }
]
~~~

### 공부한 내용 정리
- ##### List : 전체조회, 새로 생성
- ##### Detail : 특정 조회, 수정, 삭제
- ##### get_object : Detail에서 사용하고 특정 데이터들을 처리하기 전에 그 데이터가 존재하는지 검사해주는 기능
~~~python
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404
~~~   
- ##### PUT vs POST
  POST은 새로 추가 PUT 수정 
- ##### PUT 부분 필드 수정(partial = True)
~~~python
    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data, partial= True)
~~~
            
         


### 간단한 회고
FBV로 구현을 해보고 CBV로 옮기니까 훨씬 이해가 빠르게 되었고 , FBV보다 좀더 잘 정리된 느낌을 받았습니다  

## 5주차 과제 (기한: 5/13 목요일까지)

### 1. Viewset으로 리팩토링하기

- 기존에 구현했던 API를 Viewset을 이용하여 리팩토링 해주세요!
~~~python
class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
~~~

GET, POST, PUT, PATCH, DELETE 모두 잘 돌아감 

### 2. filter 기능 구현하기

~~~python
class PostFilter(FilterSet):
    text = filters.CharFilter(field_name="text", lookup_expr="icontains") #해당 문자열을 포함하는 queryset
    is_current= filters.BooleanFilter(method='filter_is_current') # true시에 이번 달 게시물만 출력 

    class Meta:
        model = Post
        fields = ['author', 'text', 'pub_date']

    def filter_is_current(self, queryset, name, value):
        set1 = queryset.filter(pub_date__year=2021)
        set2 = queryset.filter(pub_date__month=5)
        
        return set1 & set2
    
    
    class PostViewSet(viewsets.ModelViewSet):
        serializer_class = PostSerializer
        queryset = Post.objects.all()
        filter_backends = [DjangoFilterBackend]
        filter_class = PostFilter
    


 ~~~

api/contents/?text=viewset

~~~python
[
    {
        "id": 3,
        "text": "viewset해봄",
        "like": [],
        "author_nickname": "포슬포슬",
        "author": 1,
        "photos": [],
        "videos": []
    },
    {
        "id": 8,
        "text": "viewset 과제 완료 가즈",
        "like": [],
        "author_nickname": "포슬포슬",
        "author": 1,
        "photos": [],
        "videos": []
    },
    
]
~~~

api/contents/?text=viewset&is_current=true
~~~python
[
    {
        "id" 8,
        "text": "viewset 과제 완료 가즈",
        "like": [],
        "author_nickname": "포슬포슬",
        "author": 1,
        "photos": [],
        "videos": []
    },
]
~~~

### 3. (선택) **permission** 기능 구현하기

- view 중 하나 이상을 선택해 permission 기능을 구현해 보세요
    - 해당 view가 정말로 접근 권한 확인이 필요한 지, 아니면 접근 권한을 없애 보다 쉽게 접근해야 할 대상인지 고민해 본 후에 view를 선택해주세요
    - DRF에서 제공하는 permission class에 어떤 것들이 있는지 먼저 살펴본다면 좋겠죠?

### 4. (선택) validation 적용하기

- 자유롭게 validation 을 만들어 적용해보세요
- (권장) validator 만들어서 적용해보기

### 5. 배운점

- #### viewSet  
  django view -> rest_framework APIView -> Generic Views -> Viewsets
  

- #### ModelViewSet
  - Retrieve, Destory, Update -> model_name/\<int:pk>/ -> pk해당 인스턴스관련    
  
  - List, Create -> model_name/ -> 전체 get 또는 새로 post  
  
  
- #### decorator action
  ModelViewSet에서 기본 제공해주는 기능 외에 더 커스터마이징 하고싶은 경우 사용 자
  - import문 
    ~~~python
    from rest_framework.decorators import action
    ~~~
  -  action의 인자
     1. detail :  Boolean 으로서 True 일 경우, pk 값을 지정해줘야하는 경우에 사용하고 False일 경우, 목록 단위로 적용
     2. method :  request method 를 지정해줄 수 있습니다. 디폴트 값은 get  
    
  - detail에 따른 router  
    (이 때 모든 이름은 소문자이며, function name의 언더바(_)는 하이픈(-) 으로 교체)
    1. detail=True

        url : /prefix/{pk}/{function name}/  
        name : {model name}-{function name}  
       
    2. detail=False  

        url : /prefix/{function name}/  
        name : {model name}-{function name}  
   - 예
    ~~~python
      class PostViewSet(ModelViewSet):
          queryset = Post.objects.all()
          serializer_class = PostSerializer 
          
           # url : post/{pk}/set_public/
          @action(detail=True, methods=['patch'])
          def set_public(self, request, pk):
              instance = self.get_object()
              instance.is_public = True
              instance.save()
              serializer = self.get_serializer(instance)
              return Response(serializer.data)
    ~~~
  
- Router  
ViewSet은 하나의 view가 아닌 view들의 set이기 때문에 apiView와 다르게 url mapping방식에 router를 사용  
  router가 위의 코드에서 as_view로 method마다 함수로 연결해주던 것을 대신해
  - as_view이용해서 각각 매핑
    ~~~python
    class PostViewSet(ModelViewSet):
        queryset = Post.objects.all()
        serializer_class = PostSerializer   
    
    post_list = PostViewSet.as_view({
        'get': 'list',
        'post': 'create',
    })
    
    post_detail = PostViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy',
    })
    ~~~
    ~~~python
    
        urlpatterns = [
            path('post/', views.post_list),
            path('post/<int:pk>/', views.post_detail),
        ]
    ~~~
  - router를 이용하여 한번에 매핑
    ~~~python
        router = DefaultRouter()
        router.register(r'post',views.PostViewSet)
        
        urlpatterns = [
            path('',include(router.urls)),
        ]
    ~~~
  
- #### method 이용한 필터링  
  api/contents/?is_current=true
  - params  
   name = is_current  
    value = True  
    이를 이용하여 method 작성시에 if문을 사용해서 더 다양한 필터링가능
~~~python
   def filter_is_current(self, queryset, name, value):
        set1 = queryset.filter(pub_date__year=2021)
        set2 = queryset.filter(pub_date__month=5)

        return set1 & set2
~~~
### 6. 간단한회고
초반에 장고튜토리얼에서 제네릭뷰만 접했을 때도 완전 신세계였는데 viewSet이 더 끝판왕이라고 느껴졌습니다 하지만 그만큼 내부에서 어떤과정으로 
이루어지는지 쉽게 보이지 않기 때문에 그 과정을 잘 공부해야 나중에 필요에의해 커스터마이징을 잘 할 수 있고 더 잘 viewSet을 이용
할 수 있을 것 같습습니다. 이번 장이 서비스를 만들면서 더욱 완성도를 높여주기위해 필요한 것들이 많이 담겨있던 파트였다고 생각합니다. 그래서 처음접해보는 것이 많아 익혀야 할 내용이 좀 많았지만 시간이 들 더라도 꼼꼼히 보고 잘 숙지하려고 
합니다.

### 7. 참고한 곳
1. https://ssungkang.tistory.com/entry/Django-APIView-Mixins-generics-APIView-ViewSet%EC%9D%84-%EC%95%8C%EC%95%84%EB%B3%B4%EC%9E%90?category=366160
2. https://www.django-rest-framework.org/api-guide/viewsets/

