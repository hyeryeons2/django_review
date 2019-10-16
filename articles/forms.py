from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    # article 에 포함된 meta data가 작성되는 것
    class Meta:
        model = Article
        # 모든 필드를 검사한다
        fields = '__all__'