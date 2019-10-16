# django_review



### 1. 파이썬 버전 확인 및 가상환경 세팅(사전작업)

1. 파이썬 버전 확인하고 가상환경 잡기

   ```
   python -V  # V는 대문자
   venv  # python 버전이 3.7.4인지 확인하기
   
   ```

2. 장고 프로젝트 만들기

   ```
   python -m venv venv  # 파이썬의 모듈중에 가상환경(venv)를 쓰겠다는 말
   # python -m venv venv  # 뒤의 venv는 venv라는 이름이라는 명명
   # 가상환경 세팅 ok
   
   ```

3. `kill terminal` 후, `ctrl+shift+p`해서 `python interpreter > venv` 써 있는 3.7.4 파이썬 클릭

4. `ctrl+~`해서 `venv` 가상환경이 제대로 잡히는 지 확인

5. `pip list` 후 `pip` 업그레이드

6. 장고 설치(설치 후, `pip list`로 설치가 잘 되었는 지 확인)

   ```
   pip install django
   
   ```

   ** `pip freeze > requirements.txt` 하면 어떤 것들이 깔려 있고, 어떤 버전인지 확인 가능

   ```
   pip install -r requirements.txt  # requirements.txt.에 있는 라인을 한 줄씩 읽으면서 파일 내 모든 모듈을 다 설치함
   
   ```

   ** `pip freeze | xargs pip uninstall -y` 하면 pip 에 깔린 모든 것들을 삭제할 수 있음

---



### 2. 장고 프로젝트 시작

1. 프로젝트 시작

   ```
   django-admin startproject review .  # . (현재 디렉토리)에 project를 생성해주세요
   
   ```

2. 서버 확인(로켓확인)

   ```
   python manage.py runserver
   
   ```

   ** 서버끄기 `ctrl + c` , 파일저장 `ctrl + s`

3. 프로젝트 > `settings.py`에서 설정 고치기

   ```
   LANGUAGE_CODE = 'en-us' >> ko-kr 로 변경
   
   TIME_ZONE = 'UTC'  >> Asia/Seoul 로 변경
   
   USE_I18N = True  # 이걸 False로 하면 ko-kr로 해도 그냥 영어로 나오게 됨
   # 즉, language code 대로 번역할 지 말 지 결정하는 것
   
   USE_L10N = True
   
   USE_TZ = True
   
   ```

   ** 작업의 효율성을 위해 `kill terminal` 옆에 있는 `split terminal`을 사용하는 게 좋음

4. app(어플리케이션) 시작하기(articles라는 이름의 app 만든다; 보통 복수로 사용함)

   ```bash
   python manage.py startapp articles
   
   ```

5. app 생성 후, 출생신고 작업을 위해 `프로젝트>settings.py>installed_apps`에서  app 등록하기

   ```python
   INSTALLED_APPS = [
       'articles',
   ]
   
   ```

---



### 3. 데이터 모델링(models.py)

1. 모델링 작업을 위한 article 클래스 선언

   ```python
   # 이런 식으로 데이터를 제출할게요!
   class Article(models.Model):
       title = models.CharField(max_length=20)
       content = models.TextField()  # () 주의!
       created_at = models.DateTimeField(auto_now_add=True)
       # auto_now_add 데이터가 추가될 때마다 자동으로 시간 넣어줌
       updated_at = models.DateTimeField(auto_now=True)
       
   ```

2. 만든 데이터 제출 및 migrate 작업

   ```
    python manage.py makemigrations
    python manage.py migrate
   ```

   ** `ctrl+shift+p> sqllite> db.sqlite`하면 왼쪽 하단에 `sqlite explorer` 활성화됨

   ** `ipython` 확장자 설치하기

   ```
   pip install django-extensions ipython
   ```

   - 이 때, 설치한 `extensions`를 사용하기 위해서는 `settings.py>installed_apps`에 추가해야 함

     ```
     INSTALLED_APPS = [
         # local apps
         'articles',
     
         # third party apps
         'django_extensions',
     ]
     ```

### 만약에,

이미 DB 작업을 다 하고 데이터를 넣었는데, DB field를 하나 더 추가해야 한다면,

예) content 빼고 기껏 작업했는데 content 를 넣었을 때, 기존 db에 있던 content 어떻게 해야하는 지?

```
python manage.py shell_plus  # shell 사용

> from articles.models import Article 가 다다음 줄에 뜨는 지 확인
```

```
Article 치면,
articles.models.Article 이 출력되는 것을 확인할 수 있음
```

```
# artcle 인스턴스 생성(article이라는 이름으로 인스턴스 생성한다)
article = Article()
article.title = '첫 번째 타이틀'
article.save()  << 저장 필수!

```

** 종료하고 싶으면 `exit()`하면 됨

** 데이터가 잘 들어갔는 지 확인하려면, `sqlite explorer`에서 `articles_article> ▶`으로 확인 

** 데이터 작업 후, 수정하고 싶으면 `models.py`에서 추가 필드 작성 후, (`content field`를 넣는다)

```
python manage.py makemigrations 해서 필드 추가 작성을 알린다.
```

- 이러면, `you are trying to add a non-nullable field~` 메세지가 뜸

  ```
  Select an option: 1 << 1치고 엔터 << 2가지 옵션 중에 뭘 선택할거니?
  # 그럼 이미 있던 데이터의 빈 값에 뭘 넣을 것인가? >> ' ' 치고 엔터(빈스트링)
  # 다 완료됐으므로 migrate 작업하기
  python manage.py migrate
  ```

---



### 4. VS CODE SETTING workspace작업(.vscode>settings.json)

- 왼쪽 중간쯤 있는 `extensions` 탭에서 `django` 치고 `disable`된 것 확인 후, 설명 중 이 부분 찾아서 복붙

  ** 콤마 주의!

```
{
    "python.pythonPath": "venv\\Scripts\\python.exe", << 이건 원래 있던 것
    
    "files.associations": {
        "**/templates/*.html": "django-html",
        "**/templates/*": "django-txt",
        "**/requirements{/**,*}.{txt,in}": "pip-requirements"
    },
    "emmet.includeLanguages": {"django-html": "html"},
    "[django-html]": {
        "editor.tabSize": 2
    }, << 이건 따로 django tabsize를 설정하는 것이므로 추가로 적어주기(취향)
    ** tabsize:2 후 콤마 안적어도 됨!
}

```

---



### 5. 프로젝트 url 작업(review>urls.py, articles>urls.py)

```python
from django.contrib import admin
from django.urls import path, include  # include 추가

urlpatterns = [
    # articles/로 들어오면 게시글 내용 제공한다
    path('articles/', include('articles.urls')),
]
```

1. `articles` 에 `urls.py` 파일 생성하기(어플리케이션 url 작업)

   ```python
   from django.urls import path
   from . import views  # 현재 디렉토리에서 views import 한다
   
   app_name = 'articles' # 그냥 create만 쓰면 어디 app의 create인지 모르니, app_name에 articles를 추가함 (articles, create로 가)
   
   # url과 views 매핑작업
   urlpatterns = [
       # create 라는 이름으로 create url 만들게!
   	path('create/', views.create, name='create'),
   ]
   
   ```

---



### 6. Views.py 작업(articles>views.py)

1. `articles>views.py` 작업하기

2. `articles> templates` 폴더 만들고, 그 안에 `articles` 폴더 만들기

   ** 장고가 헷갈리지 않도록!
   (여러개의 `html` 만들면 `django`는 한꺼번에 모아서 찾게 됨, 따라서 `articles namespace`를 주면 articles에 있는 `html`을 쉽게 찾아서 가져올 수 있음)

3. `articles templates`에 `create.html`만들기
   ** `python manage.py runserver`에서 `articles/create/` 치면 해당 페이지를 찾아 보여줌

---



### 7. html 작업(base.html 작업)

`review> templates` 폴더 생성 후, `base.html` 파일 생성

1. `! tab` (** `block title` 위치 주의)

   ```django
   <!DOCTYPE html>
   <html lang="ko">
   <head>
     <meta charset="UTF-8">
     <meta name="viewport" content="width=device-width, initial-scale=1.0">
     <meta http-equiv="X-UA-Compatible" content="ie=edge">
     <title>{% block title %}{% endblock title %}</title>
   </head>
   <body>
     {% block container %}{% endblock container %}
   </body>
   </html>
   ```

2. `base.html` 토대로 다른 `templates> html` 파일들에 적용해보기!

3. 다시, `articles>templates>articles>create.html`으로 가서 

   ```django
   {% extends 'base.html' %}
   
   {% block title %} Article: Create{% endblock title %}
   
   {% block container %}
   <form>
     <input type="text"><br>
     <textarea name="" cols="30" rows="10"></textarea><br>
     <button type="submit">생성하기</button>
   </form>
   {% endblock container %}
   
   ```

   ** 작업 후, 서버에서 확인해 보면 `templates does not exist` 라고 뜸

   WHY?  `프로젝트(Review)> settings.py> templates> dirs` 작업을 안했기 때문!

   - `dirs` 뒤가 비어 있으니까, 위에 올려서 다음 코드 확인

     ```
     BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
     ```

   - `dirs`에 넣기

     ```
     'DIRS': [os.path.join(BASE_DIR, 'review', 'templates')],
     # join이 괄호 안에 있는 것들을 다 합친다
     ```

---



### 8. forms.py 작업(model form 작성하기)

1. `articles>forms.py` 파일 생성하기(`model form` 정의)

   ```python
   from django import forms
   from .models import Article #추가 작성 models에서 Article이라는 모듈 가져온다
   
   class ArticleForm(forms.ModelForm):
       # article 에 포함된 meta data가 작성되는 것
       class Meta:
           model = Article
           # 모든 필드를 검사한다
           fields = '__all__'
           
   ```

2. `articles<views.py`

   ```python
   from django.shortcuts import render
   from .forms import ArticleForm  ## 이거 추가
   
   def create(request):
       if request.method == 'POST':
           pass
       else:
           form = ArticleForm()  # 이거 추가(2)
           context = {'form': form}  # 이거 추가(3)
           return render(request, 'articles/create.html', context)  # context
   
   ```

3. `articles>templates>articles>create.html`

   ```django
   {% extends 'base.html' %} 
   
   {% block title %} Article: Create{% endblock title %}
   
   {% block container %}
   <form>
     {{ form.as_p }}  << 밑 form 작업 내용 날리고 이거 작성
     <button type="submit">생성하기</button>
   </form>
   {% endblock container %}
   ```

   ** `form`에서 기억해야 하는 것?(`create.html`에서)

   어디로 보낼 지, 어떤 `method`로 보낼 지  (`get/post`)

   - 어디로 보낼지? `action`에 정의 `articles`의 `create`에 보낸다
     ** url이 동일한 경우 `action`을 따로 적지 않으면 알아서 동일한 곳으로 보냄(요청 보내고자 하는 url과 현재 url이 동일함, 동일한 url이지만 대신 method로 구분함)
     (get은 그냥 페이지 보여주고 post는 데이터 작업)

   - 어떤 `method`? `db`에 영향을 미치는 것은 `post`

     ```django
     <form method="post" action="{% url 'articles:create' %}" >
         
     ```

4. `views.py`의  `form` 작업

   ```python
   from django.shortcuts import render, redirect  # redirect 추가
   from .forms import ArticleForm
   
   def create(request):
       # 만약 사용자가 보낸 method가 POST(Article을 생성해달라고 하는 요청)
       if request.method == 'POST':
           form = ArticleForm(request.POST)
           if form.is_valid():  # 유효하다면,
               form.save()
               return redirect('articles:index')
       else:  # GET이면, Article을 생성하기 위한 페이지 달라고 하는 요청
           form = ArticleForm()
           context = {'form': form}
           return render(request, 'articles/create.html', context)
       
   ```

5. index page 만들기

   - `urls.py`

   ```python
   from django.urls import path
   from . import views
   
   app_name = 'articles'
   
   urlpatterns = [
       path('', views.index, name='index'),
       path('create/', views.create, name='create'),
   ]
   
   ```

   - `views.py`

     ```python
     from django.shortcuts import render, redirect  # redirect 추가
     from .forms import ArticleForm
     from .models import Article << 추가
     
     # Create your views here.
     
     def index(request):
         articles = Article.objects.all()
         context = {'articles': articles}
         return render(request, 'articles/index.html', context)
     
     ```

   - `index.html` 작업

     ```django
     {% extends 'base.html' %}
     
     {% block title %}Article: Index{% endblock title %}
     
     {% block container %}
       <hr>
       <h2>Article list</h2>
       <a href="{% url 'articles:create' %}">[생성하기]</a>
       {% for article in articles %}
       <div>
         <h3>{{ article.pk }}. {{ article.title }}</h3>
       </div>
       <br>
       {% endfor %}
     {% endblock container %}
     
     ```

   6. `create.html`

      ```django
      {% extends 'base.html' %}
      
      {% block title %} Article: Create{% endblock title %}
      
      {% comment %} 
      {% endcomment %}
      {% block container %}
      <form method="post" action="{% url 'articles:create' %}" >
        {% csrf_token %}  << post 요청이면 꼭꼭 넣어주기!
        {{ form.as_p }}
        {% comment %} <input type="text"><br>
        <textarea name="" cols="30" rows="10"></textarea><br> {% endcomment %}
        <button type="submit">생성하기</button>
      </form>
      {% endblock container %}
      
      ```

   7. `views.py` 에서` create` 함수 수정

      ```python
      def create(request):
          if request.method == 'POST':
              form = ArticleForm(request.POST)
              if form.is_valid():  # 유효하다면,
                  form.save()
                  return redirect('articles:index')
              else:  # 유효하지 않다면, (ex. 20자짜리인데 200자가 들어간 경우,)
                  context = {'form': form}
                  return render(request, 'articles/create.html', context)
                  
          else:
              form = ArticleForm()
              context = {'form': form}
              return render(request, 'articles/create.html', context)
          
      ```

      - 중복이 있으니까, 중복 제거해서 코드를 더 깔끔하게 만들기

        ```python
        def create(request):
            if request.method == 'POST':
                form = ArticleForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect('articles:index')
            else:
                form = ArticleForm()
            context = {'form': form} # 땡기면 됨
            return render(request, 'articles/create.html', context)
        
        ```

---



### 9. detail 페이지 만들기

1. `urls.py`
   - 사용자가` url`에 번호를 보내면, `url` 번호를 확인해서 해당 번호가 들어있는 `article` 꺼내서 보여준다
   - 이 때 사용하는 것이 `Variable routing`

2. `views.py`

   - `detail` 함수 생성하기

     ```python
     from django.shortcuts import render, redirect, get_object_or_404  #  get_object_or_404 추가
     from .forms import ArticleForm
     from .models import Article
     
     def detail(request, article_pk):
         # 사용자가 url에 적어보낸 article_pk를 통해 디테일 페이지 보여준다
         # article 있다면 하나 꺼내서 보여주고 없으면 404 페이지 보여줌
         article = get_object_or_404(Article, pk=article_pk)
     
         # context에 담아야 templates로 보낼 수 있으니까, context 작업
         context = {'article': article}
         return render(request, 'article/detail.html', context)
     ## 잠깐!
     	# return render(request, 'article/detail.html', {'article': article})
         # 이렇게 나와도 전혀 상관없음(틀린게 아님!)
         
     ```

3. `detail.html` 만들기

   ```django
   {% extends 'base.html' %}
   
   {% block title %}Article: detail{% endblock title %}
   
   {% block container %}
   {% comment %} url + app name + index page {% endcomment %}
     {% comment %} <a href="{% url 'articles:index' %}">[목록]</a>  {% endcomment %}  << 이 작업을 매번 하는 게 귀찮으니 base.html에 아예 만들어서 넣기
     <h2>{{ article.title }}</h2>
     <p>{{ article.created_at }}</p>
     <hr>
     <p>{{ article.content }}</p>
     <hr>
     <button type="submit"></button>
   
   {% endblock container %}
   ```

   ** 계속 목록 태그를 넣어야 하는게 귀찮으니까, 아예 base.html에 목록 코드 넣기

   ```django
   <!DOCTYPE html>
   <html lang="ko">
   <head>
     <meta charset="UTF-8">
     <meta name="viewport" content="width=device-width, initial-scale=1.0">
     <meta http-equiv="X-UA-Compatible" content="ie=edge">
     <title>{% block title %}{% endblock title %}</title>
   </head>
   <body>
     <header>
       <h1>페이지에 오신 걸 환영합니다:)</h1>
       <a href="{% url 'articles:index' %}">[목록]</a>  << 이 작업
       <hr>
     </header>
     {% block container %}{% endblock container %}
   </body>
   </html>
   
   ```

   ** index에서 역순으로 데이터를 보여주고 싶음. 따라서 `articles>models.py`에서 `class Meta` 작업

   ```python
   from django.db import models
   
   class Article(models.Model):
       title = models.CharField(max_length=20)
       content = models.TextField()
       created_at = models.DateTimeField(auto_now_add=True)
       updated_at = models.DateTimeField(auto_now=True)
   
       class Meta:  # 이거 작성! 1 2 3 4 를 4 3 2 1 로 보여주는 것
           ordering = ('-pk', )
           
   ```

   ** index 페이지에 상세보기 만들기

   ``` django
   {% extends 'base.html' %}
   
   {% block title %}Article: Index{% endblock title %}
   
   {% block container %}
     <hr>
     <h2>Article list</h2>
     <a href="{% url 'articles:create' %}">[생성하기]</a>
     {% for article in articles %}
     <div>
       <h3>{{ article.pk }}. {{ article.title }}</h3>
       {% comment %} article:detail 페이지로 넘어간다. {% endcomment %}
       <a href=" {% url 'articles:detail' article.pk %} ">[상세보기]</a>
     </div>
     <br>
     {% endfor %}
   {% endblock container %}
   
   ```

   

---



### 10. update 페이지 만들기

1. `urls.py`

   ```python
   from django.urls import path
   from . import views
   
   app_name = 'articles'
   
   urlpatterns = [
       # 작성!
       path('<int:article_pk>/update/', views.update, name='update'),
       
       path('<int:article_pk>', views.detail, name='detail'),
       path('', views.index, name='index'),
       path('create/', views.create, name='create'),
   ]
   ```

2. `views.py`(`model form` 활용)

   ```python
   def update(request, article_pk):
       # 3번 article을 update할 때 있으면 수정, 아니면 404 보여주기
       article = get_object_or_404(Article, pk=article_pk)
       # get일 때와 post일 때 나눠서 작업해야함
       if request.method == 'POST':
           pass
       else:  # get
           # form에 아무것도 넣지 않으면 빈칸으로 form이 보여짐
           # instance에 article을 넣으면, article에 있던 내용이 저장된 채로 보여짐
         
           # 즉, form 안에 특정 article 담아서 생성하겠다
           form = ArticleForm(instance=article)  
           # 위에서 정의한 form을 context로 넘겨줌
           context = {'article': article}
           return render(request, 'articles/update.html', context)
   
   ```

3. `update` 페이지 만들기(`create.html`이랑 동일하니 복붙)

   ```django
   {% extends 'base.html' %}
   
   {% block title %} Article: Create{% endblock title %}
   
   {% block container %}
   <form method="POST" action="{% url 'articles:create' article.pk %}" >
     {% csrf_token %}
     {{ form.as_p }}
     <button type="submit">생성하기</button>
   </form>
   {% endblock container %}
   ```

4. (추가작업) `detail` 페이지에서 [수정하기] 만들기

```django
{% extends 'base.html' %}

{% block title %}Article: detail{% endblock title %}

{% block container %}
  <h2>{{ article.title }}</h2>
  <p>{{ article.created_at }}</p>
  <hr>
  <p>{{ article.content }}</p>
  <hr>
  <a href=" {% url 'articles:update' article.pk %} ">[수정하기]</a>  << 이 작업

{% endblock container %}
```

5. `views.py`에서 `update` 함수 완성하기

   ```python
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
   
   ```

---



### 11. delete 페이지 만들기

1. `urls.py`

   ```python
   from django.urls import path
   from . import views
   
   app_name = 'articles'
   
   urlpatterns = [
       path('<int:article_pk>/delete/', views.delete, name='delete'),
       
   ```

2. `views.py`

   ```python
   def delete(request, article_pk):
       # article_pk에 맞는 article을 꺼내서 삭제함
       # 삭제할 article 꺼내는 작업
       article = get_object_or_404(Article, pk=article_pk)
       # article 이 있다면(no 404 page) 삭제
       article.delete()
       return redirect('articles:index')
   
   ```

3. `detail.html`에서 delete 가능한 `form` 작성하기

   ```django
   {% extends 'base.html' %}
   
   {% block title %}Article: detail{% endblock title %}
   
   {% block container %}
   {% comment %} url + app name + index page {% endcomment %}
     {% comment %} <a href="{% url 'articles:index' %}">[목록]</a>  {% endcomment %}
     <h2>{{ article.title }}</h2>
     <p>{{ article.created_at }}</p>
     <hr>
     <p>{{ article.content }}</p>
     <hr>
     <a href=" {% url 'articles:update' article.pk %} ">[수정하기]</a>
     
   
     # 이 작업
     {% comment %} /articles/3/delete/로 보내야 하니까 action {% endcomment %}
     <form action=" {% url 'articles:delete' article.pk %} " method="POST">
     {% csrf_token %}
     <button type="submit">[삭제하기]</button>
     </form>
   ```

4. 해당 함수가 무조건 GET 혹은 POST method로만 보내질 수 있게 하는 작업

   ```
   django require post decorator
   ```

   - `views.py`(작업 후, 코드)

     ```python
     from django.views.decorators.http import require_POST, require_GET
     
     @require_GET
     def index(request):
         articles = Article.objects.all()
         context = {'articles': articles}
         return render(request, 'articles/index.html', context)
     
     @require_GET
     def detail(request, article_pk):
         article = get_object_or_404(Article, pk=article_pk)
         context = {'article': article}
         return render(request, 'articles/detail.html', context)
     
     def create(request):
         if request.method == 'POST':
             form = ArticleForm(request.POST)
             if form.is_valid():  # 유효하다면,
                 form.save()
                 return redirect('articles:index')
         else:
             form = ArticleForm()
         context = {'form': form}
         return render(request, 'articles/create.html', context)
     
     # /articles/3/update
     def update(request, article_pk):
         article = get_object_or_404(Article, pk=article_pk)
         if request.method == 'POST':
             form = ArticleForm(request.POST, instance=article)
             if form.is_valid():
                 form.save()
                 return redirect('articles:detail', article_pk)
         else:
             form = ArticleForm(instance=article)
         context = {'form': form}
         return render(request, 'articles/update.html', context)
     
     @require_POST
     def delete(request, article_pk):
         article = get_object_or_404(Article, pk=article_pk)
         article.delete()
         return redirect('articles:index')
     ```

     

     