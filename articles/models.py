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
