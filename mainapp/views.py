from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
from .emailfuntion import *





# Create your views here.
def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is None:
            try:
                user = User.objects.get(email=username)
                user = authenticate(request, username=user.username, password=password)
            except User.DoesNotExist:
                pass 
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            messages.info(request,"Password or Username is incorrect") 

    return render(request,'base/login.html')
def signuppage(request):
    try:
        if request.method == 'POST':
            username=request.POST.get('username')
            print(username)
            password=request.POST.get('password')
            print(password)
            email=request.POST.get('email')
            print(email)
        try:
            if User.objects.filter(username=username).first():
                messages.success(request,"User with this username already exist")
                print("username")
                return redirect('/signup/')
            if User.objects.filter(email=email).first():
                messages.success(request,'User with this email already exist')
                print("email")
                return redirect('/signup/')
            user_obj=User(username=username,email=email)
            user_obj.set_password(password)
            user_obj.save()
            profile_obj=Profile.objects.create(user=user_obj)
            profile_obj.save()
            return redirect('/login/')
        except Exception as e:
            print (e)
    except Exception as e:
            print (e)
    
    return render(request,'base/signup.html')


def home(request):
    return render(request,'base/home.html')
import uuid
def forgetpassword(request):
    try:
        if request.method == 'POST':
            username=request.POST.get('username')
            if not User.objects.filter(username=username).first():
                messages.success(request,"User with this username doesnot exist")
                return redirect('/forgetpassword/')
            user_obj = User.objects.get(username=username)
            token =str(uuid.uuid4())
            profile_obj=Profile.objects.get(user=user_obj)
            profile_obj.forget_password_token=token
            profile_obj.save()
            send_forget_password_email(user_obj.email,token)
            messages.success(request,"An email has been sent to your email address.")
            return redirect('/forgetpassword/')
    except Exception as e:
        print(e)



    return render(request,'base/forgetpassword.html')

def resetpassord(request,token):
    
    try:
        profile_obj=Profile.objects.filter(forget_password_token=token).first()
        if request.method=='POST':
            new_password=request.POST.get('new-password')
            confirm_password=request.POST.get('confirm-password')
            user_id=request.POST.get('user_id')
            if user_id is None:
                messages.success(request,'No user id found')
                return redirect(f"/resetpassword/{token}/")
            if new_password != confirm_password:

                messages.success(request,'Two password fields doesnot match!')
                return redirect(f"/resetpassword/{token}/")
            user_obj=User.objects.get(id=user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('/login/')


    except Exception as e:
        print(e)

    context={'user_id':profile_obj.user.id}
    return render(request,'base/changepassword.html',context)