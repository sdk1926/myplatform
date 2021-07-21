from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password,check_password
from .models import Accounts
from django.db import transaction
import requests


def index(request):
    message={}
    if 'user' in request.session:
        message['id'] = request.session['user']
    return render(request, 'accounts/index.html', message)

def signup(request):
    if request.method == 'GET':
        return render(request, 'accounts/signup.html')

    elif request.method == 'POST':
        res_data = {}
        useremail = request.POST.get('email', None)
        userid = request.POST.get('user_id', None)
        password = request.POST.get('password', None)
        re_password = request.POST.get('password2', None)
        
        if not (useremail and userid and password and re_password):
            res_data['error'] = '모든 값을 입력해주세요.'
            return render(request, 'accounts/signup.html', res_data)
             
        if len(userid) > 128 or len(userid) < 6:
            res_data['error'] = '아이디는 6자이상 128자 이하로 만들어야 합니다.'
            return render(request, 'accounts/signup.html', res_data) 
            

        if Accounts.objects.filter(user_id=userid).exists():
            res_data['error'] = '이미 등록된 아이디입니다.'
            return render(request, 'accounts/signup.html', res_data) 
        
        if password != re_password:
            res_data['error'] = '비밀번호가 다릅니다.'
            return render(request, 'accounts/signup.html', res_data) 
        
        if len(password) > 2048 or len(password) < 8:
            res_data['error'] = '비밀번호는 8자 이상 2048자 이하여야 합니다.'
            return render(request, 'accounts/signup.html', res_data) 
 
        elif password==re_password:
            with transaction.atomic():
                accounts= Accounts(
                    user_id = userid,
                    password = make_password(password),
                    email = useremail,
                )
                accounts.save()
                return redirect('login')


def login(request):
    if 'user' in request.session:
        return redirect('index')
        
    if request.method == 'GET':
        return render(request, 'accounts/login.html')

    elif request.method == 'POST':
        #user = Accounts.objects.all()
        try:
            error_message = {}
            userid = request.POST.get('user_id', None)
            password = request.POST.get('password', None)
            user = Accounts.objects.get(user_id=userid)
        except:
            error_message['error'] = '등록되지 않은 아이디 입니다.'
            return render(request, 'accounts/login.html', error_message)
        else:
            if not check_password(password, user.password):
                error_message['error'] = '잘못된 비밀번호입니다.'
                return render(request, 'accounts/login.html', error_message)
        
        request.session['user'] = user.user_id 

        return redirect('index')


def logout(request):
    if 'user' in request.session:
        del request.session['user']
        return redirect('index')
    return redirect('index')


def kakao_signup(request):
    AUTHORIZATION_CODE = request.GET.get('code',None)
    REST_API_KEY = "f69e56958014d271373defb6cd2bbdc7"    
    REDIRECT_URI = "http://127.0.0.1:8000/accounts/kakaologin/"
    token_request = requests.post(f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&code={AUTHORIZATION_CODE}").json()
    access_token = token_request['access_token']
    kakao_user_info = requests.post("https://kapi.kakao.com/v2/user/me", headers={"Authorization" : f"Bearer {access_token}"},).json()
    kakaoid = kakao_user_info.get('id',None)
    kakaoid = int(kakaoid)
    kakaoaccounts = kakao_user_info.get('kakao_account')
    if Accounts.objects.filter(user_id=kakaoid).exists():
        user = Accounts.objects.get(user_id=kakaoid)
        request.session['user'] = user.user_id
        return redirect('index')
    else:
        kakao_accounts = Accounts(
            user_id= kakaoid,
            email = kakaoaccounts.get('email',None),
            password = make_password(str(kakaoid)),
        )
        kakao_accounts.save()
        user = Accounts.objects.get(user_id=kakaoid)
        request.session['user'] = user.user_id
        return redirect('index')
    
def kakao_del(request):
    AUTHORIZATION_CODE = request.GET.get('code',None)
    REDIRECT_URI = "http://127.0.0.1:8000/accounts/kakaokill/"
    REST_API_KEY = "f69e56958014d271373defb6cd2bbdc7"    
    token_request = requests.post(f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&code={AUTHORIZATION_CODE}").json()
    access_token = token_request['access_token']
    requests.post("https://kapi.kakao.com//v1/user/unlink", headers={"Authorization" : f"Bearer {access_token}"},).json()
    return redirect('index')
    









        

