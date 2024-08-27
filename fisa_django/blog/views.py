from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from .models import Post
## blog/views.py
from django.views.generic import ListView, DetailView, CreateView
from .models import Post
from django.db.models import Avg, Max, Min, Sum

class PostCreate(CreateView):
    model = Post
    fields = ["title","content","head_image"]

    #이미 craeteview가 내장된 함수 -- 오버라이딩
    #tag는 참조관계이므로 tag테이블에등록된 태그만 쓸수 있는 상황
    #임의로 방문가 form에 Tag를 달아서 보내도록 form_valid에 결과를 담아두고 저장된 포스트로 돌아오도록
        # CreateView가 내장한 함수 - 오버라이딩 
    # tag는 참조관계이므로 Tag 테이블에 등록된 태그만 쓸 수 있는 상황
    # 임의로 방문자가 form에 Tag를 달아서 보내도록 form_valid()에 결과를 임시로 담아두고
    # 저장된 포스트로 돌아오도록 
    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            response = super(PostCreate, self).form_valid(form)

            tags_str = self.request.POST.get('tags_str')
            if tags_str:
                tags_str = tags_str.strip()

                tags_str = tags_str.replace(',', ';')
                tags_list = tags_str.split(';')

                for t in tags_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(tag_name=t)
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tag.add(tag)




class PostList(ListView):   # post_list.html, post-list
    model = Post 
    # template_name = 'blog/index.html' 
    ordering = '-pk' 
    context_object_name = 'post_list'


class PostDetail(DetailView):   # post_list.html, post-list
    model = Post 
    # template_name = 'blog/index.html' 
    ordering = '-pk' 
    context_object_name = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = '임의로 작성한 새로운 변수'
        print(context)
        return context
# Create your views here.


def index(request):
    posts = Post.objects.all() # 1. 쿼리로 데이터를 모두 가져옵니다
    # 가져온 데이터는 어디에 뿌려야 하나요? Templates로 보내야겠죠
    return render(
        request,
        'blog/index.html',
        {
            'posts':posts,'my_list': ["apple", "banana", "cherry"], 'my_text': "첫번째 줄 \n 두번째 줄", 'content' : '<img src ="data/b1.jpg">' ,
        }
    )

def about_me(request):
    return render(
        request,
        'blog/about_me.html'
    )