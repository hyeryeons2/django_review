from django.shortcuts import render, redirect
# 사용자한테 데이터 받는 과정(장고에서 제공하는 form 활용)
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
# as auth_login으로 하는 이유? import login과 def login 이름이 겹침
from django.contrib.auth import login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import CustomUserChangeForm


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
    return render(request, 'accounts/form.html', context)
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
    return render(request, 'accounts/form.html', context)


def logout(request):
    auth_logout(request)
    return redirect('articles:index')


@require_POST
# 유저 삭제(회원탈퇴)
def delete(request):
    request.user.delete()
    return redirect('articles:index')


# 유저 정보 업데이트
# UserChangeForm
@login_required
def update(request):
    if request.method == 'POST':
        # 수정해주세요 요청 들어오면,
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:  # get 요청
    # 수정할 수 있는 페이지 주세요 요청 들어오면,
    # request.user에서 사용자 기본 정보 들어 있는 상태로 form 보여준다
        form = CustomUserChangeForm(instance=request.user)
        # context> templates로 넘기기 위해
    context = {'form': form}
    return render(request, 'accounts/form.html', context)


@login_required
# 비밀번호 변경함수(PasswordChangeForm)
def password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # 비밀번호 바뀌면, session에 update 한다(비밀번호 변경하면 로그인 상태 유지)
            update_session_auth_hash(request, user)
            return redirect('accounts:update')
        # valid 하지 않은 경우, form 담아서 그 페이지 보여줌
    else:
        # request.user을 담아서 보낸다(기존 방식과 다름)
        form = PasswordChangeForm(request.user)
    context = {'form': form}
    return render(request, 'accounts/password.html', context)
# 비밀번호 변경하면, 로그아웃이 됨. 기존 데이터와 다르기 때문