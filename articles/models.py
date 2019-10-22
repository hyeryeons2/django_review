from django.db import models
from django.conf import settings  # setting에 기본 저장되어 있는 user model 불러오는 작업

# article.liked_users.all()
# user.liked_articles.all()
# article.user을 쓸 수 있게 됨 (user의 Foreignkey 설정)
class Article(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # auto_now_add 데이터가 추가될 때마다 자동으로 시간 넣어줌
    updated_at = models.DateTimeField(auto_now=True)

    # 한명의 USER가 article을 여러개 작성한다 (M:N)
    # USER 정보가 없어지면, Article 정보도 없어진다.
    # 다른 모든 곳에서는 get_user_model로 가져오되, models.py에서 user을 가져올 땐 django setting의
    # default 된 user model을 가져와야 함
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # 좋아요 누른 유저
    liked_users = models.ManyToManyField(  # article.liked_users.all() => 아티클을 좋아하는 모든 유저
        settings.AUTH_USER_MODEL, 
        related_name='liked_articles',) # user.liked_articles.all() => 유저가 좋아하는 모든 아티클 유저)

    class Meta:
        ordering = ('-pk', )

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # article 참조키(foreign key)
    # relatedname은 나중에 views.py>detail 에서 comments = article.comments.all()
    # article.comment_set.all()로 받아와야 하지만,
    # related_name 설정을 통해 article.comments.all()로 가져올 수 있게 됨
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return self.content
