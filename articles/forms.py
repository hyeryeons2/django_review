from django import forms
from .models import Article, Comment

class ArticleForm(forms.ModelForm):
    # article 에 포함된 meta data가 작성되는 것
    class Meta:
        model = Article
        # 모든 필드를 검사한다
        fields = '__all__'

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='comment',
        )
    class Meta:
        model = Comment
        # fields를 all로 하면, article 선택창이 뜸
        fields = ['content', ]
        # exclue = ['article', ] 로 해도 됨
