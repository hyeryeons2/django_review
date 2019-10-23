from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model  # 현재 활성화(active)된 user model을 return 한다
# Why? default user model이 있는데 나중에 customizing 할 user model을 만들게 되면 그때에는 default user model이 아니라 
# customizing 한 user model 을 불러오기 위한 작업: customizing 한 user모델을 등록하게 되면 이 때에는 get_user_model이 default 가 아니라 customizing 한 유저모델로 바뀜

# userchangeform을 가지고 있는 채로 새로운 class 선언
class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        # 사용자가 수정할 수 있는 filed 지정하기
        fields = ['email', 'first_name', 'last_name', ]


# cutomizing 한 유저 모델을 인식하지 못해서 직접 usercreationform을 지정해야 함
# 원래는 usercreationsform을 쓰면 회원가입이 가능했음

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields