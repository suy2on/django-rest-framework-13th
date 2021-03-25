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
shell에서 작성한 코드와 그 결과를 보여주세요!

### 간단한 회고
과제 시 어려웠던 점이나 느낀 점, 좋았던 점 등을 간단히 적어주세요!
