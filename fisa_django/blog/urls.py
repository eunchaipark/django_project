from django.urls import path
from . import views

urlpatterns = [
    # blog 앱 내부의 경로를 지정할 부분
    path('', views.index), # localhost:8000/blog 없는 경로를 호출하고 있음  , 경로, 경로를 호출하면 실행할 함수의 위치
    path('post_list',views.PostList.as_view()),
    path('about_me', views.about_me),
    path('<int:pk>', views.PostDetail.as_view()),  #동적으로 변경되는 부분은 꺽쇠로 표현한다
    path('create-post/',views.PostCreate.as_view()),
]
