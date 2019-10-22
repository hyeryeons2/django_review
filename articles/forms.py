from django import forms
from .models import Article, Comment

class ArticleForm(forms.ModelForm):
    # article 에 포함된 meta data가 작성되는 것
    class Meta:
        model = Article
        # form에서 all 필드 설정하면 user form까지 보임
        # 모든 필드를 선택하는 것이 아닌, title과 content만 보이게!
        fields = ['title', 'content', ]

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='comment',
        )
    class Meta:
        model = Comment
        # fields를 all로 하면, article 선택창이 뜸
        fields = ['content', ]
        # exclue = ['article', ] 로 해도 됨
