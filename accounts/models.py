from django.db import models
from django.conf import settings  # settings.AUTH.USER_MODEL 쓰기 위한 작업
from django.contrib.auth.models import AbstractUser # 유저모델 customizing 하기 위한 import 작업

# reservation class 중개 모델을 만들었을 때, 
# doctor.reservation_set.all() 를 매번 써야해서 불편했음
# doctor.patients.all()로 바로 접근(manytomany)

# User customizin'(유저와 유저간의 m:n; 팔로우)
class User(AbstractUser):
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        # many to many 모델에는 related_name이 필요함
        related_name='followings',
        )


