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
     

* Post  
written : 글  
  pub_date : 업로드날짜   
  author_id : 글쓴이   
      

* Video  
video : 동영상  
  post_id : 소속게시물    
    
  
* Photo  
image : 사진   
  post_id : 소속게시물 

  

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

post의 author조회 
~~~python
>>> post1.author
<User: user1>
>>> post1.author.username
>>> 'user1'
~~~
user1의 post 조회하기 
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
과제 시 어려웠던 점이나 느낀 점, 좋았던 점 등을 간단히 적어주세요!
