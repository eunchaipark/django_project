from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# models모듈의 Model 클래스를 상속받는 자식클래스 생성

class Tag(models.Model):
    #id 즉 PK는 자동생성됨
    tag_name =models.CharField(max_length=30,unique=True) #다 대 다 설정함
    slug = models.SlugField(max_length=30,unique=True,allow_unicode=True) #찌꺼기라는 뜻의 slug 여기서는 문자, 숫자 ,하이푼만을 포함하는 문자열인데 일반적으로 URL에 사용한다.

    def __str__(self):
        return self.tag_name

    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}'





class Post(models.Model): 
    title = models.CharField(max_length=50)
    content = models.TextField()
		
	# django model 이 최초 저장(insert) 시에만 현재날짜(date.today()) 를 적용
    # 아예 값 자체가 지금 시간으로 입력되어 들어감(우리가 변경할 필요 없음)
    created_at = models.DateTimeField(auto_now_add=True)   #now()
    updated_at = models.DateTimeField(auto_now=True)
	# django model 이 save 될 때마다 현재날짜(date.today()) 로 갱신됨
    
    # blog/models.py
    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    # blank=True - 필수 항목 아님이라는 파라메터

    #외래키와 프라이머리키의 관계
    # cascade 관련된 글은 다 삭제
    # SET_NULL이라는 옵션을 ㅜ저서 user가 삭제되면 관련있는 post테이블의 모든 글에 author항복이 null로 바뀜
    author = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

    tag= models.ManyToManyField(Tag)

    # blog/models.py
    def __str__(self):
        return f'[[{self.pk}] {self.title}]'
    
    def get_absolute_url(self):
        return f'/blog/{self.pk}'
		


class comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)  #하나의 포스트에 여러개의 외래키를 걸어준다.
    author=models.ForeignKey(User,on_delete=models.CASCADE)  #여러사람이 하나의 댓글창에 댓글 달기 가능
    content = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)   #now()
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return f'[[{self.pk}] {self.title}]'
    
    def get_absolute_url(self): 
        return f'{self.post.get_absolute_url()}#comment-{self.pk}' # #을 단 이유 : html에서 ID 
