from django.shortcuts import render, redirect
# 사용자한테 데이터 받는 과정(장고에서 제공하는 form 활용)
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# as auth_login으로 하는 이유? import login과 def login 이름이 겹침
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.views.decorators.http import require_POST


def signup(request):
    # 만약에 user가 인증 상태에서 sign 요청 보내면,
    if request.user.is_authenticated:
        return redirect('articles:index')
    if request.method == 'POST':
        # 회원가입 로직
        # get에서 보낸 데이터 from을 post로 받고
        form = UserCreationForm(request.POST)
        # 유효성 검사후, 통과하면 저장하기
        if form.is_valid():
            form.save()
            # 회원가입하면 자동 로그인 상태로 보이는 페이지
            user = form.save()
            auth_login(request, user)
            return redirect('articles:index')
    else:
        # usercreationform을 context로 저장해서 signup html에서 보여준다
        form = UserCreationForm()
    # get, post 둘다 실행 가능
    context = {'form': form}
    return render(request, 'accounts/signup.html', context)
# 회원가입이 제대로 되었는 지 확인하기 위해서는 admin 페이지에서 관리자 로그인 후,
# python manage.py createsuperuser 
# 사용자(들) 에서 회원 목록을 확인할 수 있음


# 로그인은 session data 한 줄을 만들어 주는 것
def login(request):
    if request.user.is_authenticated:
        return redirect('articles:index')
    # post 로그인 시켜준다
    if request.method == 'POST':
        # 주의!! AuthenticationForm은 requst, request.POST로 내야함
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            # 로그인 시키는 과정
            auth_login(request, form.get_user())

            # ★★★★login required 때문에 next page로 보내짐
            # ★★★★next_page가 있으면 next page로 보내고 아니면 index 페이지로 보내세요
            # login 끝나면 create로 보내세요
            next_page = request.GET.get('next')
            #redirect는 get method(요청)에만 가능
            return redirect(next_page or 'articles:index')
        # invalid 한 경우, 그냥 context에 form을 넣어서 보내줌
    else: # get 로그인 할 수 있는 페이지 제공
        form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'accounts/login.html', context)


def logout(request):
    auth_logout(request)
    return redirect('articles:index')


@require_POST
# 유저 삭제(회원탈퇴)
def delete(request):
    request.user.delete()
    return redirect('articles:index')