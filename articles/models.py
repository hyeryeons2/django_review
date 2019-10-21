from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # auto_now_add 데이터가 추가될 때마다 자동으로 시간 넣어줌
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-pk', )

class Comment(models.Model):
    # article 참조키(foreign key)
    # relatedname은 나중에 views.py>detail 에서 comments = article.comments.all()
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return self.content

