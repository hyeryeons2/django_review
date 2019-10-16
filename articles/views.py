from django.shortcuts import render

# Create your views here.

def create(request):
    # 만약 사용자가 보낸 method가 POST(Article을 생성해달라고 하는 요청)
    if request.method == 'POST':
        title = request.POST.get('title')
    else:  # GET이면, Article을 생성하기 위한 페이지 달라고 하는 요청
        return render(request, 'articles/create.html')
