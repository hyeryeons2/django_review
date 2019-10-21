from django.shortcuts import render, redirect, get_object_or_404  # redirect 추가
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import ArticleForm, CommentForm
from .models import Article, Comment
from IPython import embed 


@require_GET
def index(request):
    # embed()
    articles = Article.objects.all()
    context = {'articles': articles}
    return render(request, 'articles/index.html', context)

@require_GET
def detail(request, article_pk):
    # 사용자가 url에 적어보낸 article_pk를 통해 디테일 페이지 보여준다
    # article 있다면 하나 꺼내서 보여주고 없으면 404 페이지 보여줌
    article = get_object_or_404(Article, pk=article_pk)
    # commentform에 맞는 form 형식받는 것;get
    form = CommentForm()
    # 해당 article pk 에 있는 comments를 모두 가져온다
    comments = article.comments.all()
    # 혹은, comments = Comment.objects.all()로도 사용함

    # context에 담아야 templates로 보낼 수 있으니까, context 작업
    context = {
        'article': article,
        'form': form,
        'comments': comments,
        }
    return render(request, 'articles/detail.html', context)
    # return render(request, 'article/detail.html', {'article': article})
    # 이렇게 나와도 전혀 상관없음(틀린게 아님!)

# 로그인 된 상태에서만 CREATE 실행
@login_required
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

@login_required  # get 요청 있는 경우에만 login_required 가능
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

# login_required 는 get 요청에만 가능하므로 POST에는 쓸 수 없음
# @login_required
# /articles/3/delete/
@require_POST
def delete(request, article_pk):
    # 함부로 delete 하지 못하게 하기 위해 POST method 해줘야 함

    if request.user.is_authenticated:
    # article_pk에 맞는 article을 꺼내서 삭제함
    # 삭제할 article 꺼내는 작업
        article = get_object_or_404(Article, pk=article_pk)
    # article 이 있다면(no 404 page) 삭제
        article.delete()
    return redirect('articles:index')


# detail 페이지에서 다 처리할 것이기 때문에 get이 따로 없으므로
# require_POST 처리함
# @login_required ; post ㄴㄴ 
@require_POST
def comments_create(request, article_pk):
    if request.user.is_authenticated:
        form = CommentForm(request.POST)

        if form.is_valid():
            # 완전히 db에 반영하지는 말자 commit=False(임시저장)
            comment = form.save(commit=False)
            comment.article_id = article_pk
            # 이 작업이 끝나면 comment에 content와 id가 다 들어가고, 그걸 저장한다
            comment.save()
        # 유효하든, 유효하지않든 이 화면 보여준다
    return redirect('articles:detail', article_pk)


# @login_required
@require_POST
def comments_delete(request, article_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        comment.delete()
    # article = get_object_or_404(Article, pk=article_pk) 안했으니까
    # article.pk 못씀
        return redirect('articles:detail', article_pk)
        
    # 401 code == 인증되지 않았다
    # 이 설정 후, 쿠키>session 삭제하면, 로그아웃이 되고, 그 상태에서 댓글 삭제를 하면 
    # 401 페이지와 함께 you are Unauthorized 가 출력됨
    return HttpResponse('You are Unauthorized', status=401)