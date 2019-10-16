from django.shortcuts import render, redirect, get_object_or_404  # redirect 추가
from django.views.decorators.http import require_POST, require_GET
from .forms import ArticleForm
from .models import Article
# from IPython import embed 

# Create your views here.

@require_GET
def index(request):
    articles = Article.objects.all()
    context = {'articles': articles}
    return render(request, 'articles/index.html', context)

@require_GET
def detail(request, article_pk):
    # 사용자가 url에 적어보낸 article_pk를 통해 디테일 페이지 보여준다
    # article 있다면 하나 꺼내서 보여주고 없으면 404 페이지 보여줌
    article = get_object_or_404(Article, pk=article_pk)

    # context에 담아야 templates로 보낼 수 있으니까, context 작업
    context = {'article': article}
    return render(request, 'articles/detail.html', context)
    # return render(request, 'article/detail.html', {'article': article})
    # 이렇게 나와도 전혀 상관없음(틀린게 아님!)


def create(request):
    # 만약 사용자가 보낸 method가 POST(Article을 생성해달라고 하는 요청)
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        # embed()  # 실행중 python shell 실행
        if form.is_valid():  # 유효하다면,
            form.save()
            return redirect('articles:index')
        # else:  # 유효하지 않다면,(ex. 20자짜리인데 200자가 들어간 경우,))
        #     context = {'form': form}
        #     return render(request, 'articles/create.html', context)

    else:  # GET이면, Article을 생성하기 위한 페이지 달라고 하는 요청
        form = ArticleForm()
    context = {'form': form}
    return render(request, 'articles/create.html', context)

# /articles/3/update
def update(request, article_pk):
    # 3번 article을 update할 때 있으면 수정, 아니면 404 보여주기
    article = get_object_or_404(Article, pk=article_pk)
    # get일 때와 post일 때 나눠서 작업해야함

    # POST 로 들어오면 UPDATE 로직을 수행한다
    if request.method == 'POST':
        # model form 활용
        # 기존에 받은 instance(article)을 form에 추가한다
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('articles:detail', article_pk)
    else:  # get
        # model form 활용
        # form에 아무것도 넣지 않으면 빈칸으로 form이 보여짐
        # instance에 article을 넣으면, article에 있던 내용이 저장된 채로 보여짐
        form = ArticleForm(instance=article)  # form 안에 특정 article 담아서 생성하겠다
        # 위에서 정의한 form을 context로 넘겨줌
    context = {'form': form}
    return render(request, 'articles/update.html', context)

# /articles/3/delete/
@require_POST
def delete(request, article_pk):
    # 함부로 delete 하지 못하게 하기 위해 POST method 해줘야 함

    # article_pk에 맞는 article을 꺼내서 삭제함
    # 삭제할 article 꺼내는 작업
    article = get_object_or_404(Article, pk=article_pk)
    # article 이 있다면(no 404 page) 삭제
    article.delete()
    return redirect('articles:index')