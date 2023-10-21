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
    tweets = Tweetsdata.objects.all()
    if request.method == 'POST':
        form = TweetScrapeForm(request.POST)
        if form.is_valid():
            keywords = form.cleaned_data['keywords']
            num_tweets = form.cleaned_data['num_tweets']

           
            scrapedata(keywords, num_tweets)

    else:
        form = TweetScrapeForm()
    context={'tweets':tweets,'form': form}
    return render(request,'base/home.html',context)
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





import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import pandas as pd

from .forms import *




    
def scrapedata(keywords, num_tweets):
    PATH = r"C:\Users\786\Desktop\chromedriver-win64\chromedriver.exe"# your path to chrome driver
    driver = webdriver.Chrome(PATH)
    driver.get("https://twitter.com/login")


    subject = keywords


    
    sleep(10)
    username = driver.find_element(By.XPATH,"//input[@name='text']")
    username.send_keys("")# your user name
    next_button = driver.find_element(By.XPATH,"//span[contains(text(),'Next')]")
    next_button.click()

    sleep(60)
    password = driver.find_element(By.XPATH,"//input[@name='password']")
    password.send_keys('')# YOUr password 
    log_in = driver.find_element(By.XPATH,"//span[contains(text(),'Log in')]")
    log_in.click()

    
    sleep(30)
    search_box = driver.find_element(By.XPATH,"//input[@data-testid='SearchBox_Search_Input']")
    search_box.send_keys(subject)
    search_box.send_keys(Keys.ENTER)


    sleep(10)
    UserTags = []
    TimeStamps = []
    Tweets = []
    Replys = []
    reTweets = []
    Likes = []
    articles = driver.find_elements(By.XPATH,"//article[@data-testid='tweet']")

    unique_tweet_set = set()  
    while len(unique_tweet_set) < num_tweets:  
        for article in articles:
            UserTag = article.find_element(By.XPATH, ".//div[@data-testid='User-Name']").text
            TimeStamp = article.find_element(By.XPATH, ".//time").get_attribute('datetime')
            Tweet = article.find_element(By.XPATH, ".//div[@data-testid='tweetText']").text

           
            tweet_data = (UserTag, TimeStamp, Tweet)
            if tweet_data not in unique_tweet_set:
                UserTags.append(UserTag)
                TimeStamps.append(TimeStamp)
                Tweets.append(Tweet)
                Replys.append(article.find_element(By.XPATH, ".//div[@data-testid='reply']").text)
                reTweets.append(article.find_element(By.XPATH, ".//div[@data-testid='retweet']").text)
                Likes.append(article.find_element(By.XPATH, ".//div[@data-testid='like']").text)
                unique_tweet_set.add(tweet_data)

        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        sleep(3)
        articles = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")


    print(len(UserTags),
    len(TimeStamps),
    len(Tweets),
    len(Replys),
    len(reTweets),
    len(Likes))


    

    df = pd.DataFrame(zip(UserTags,TimeStamps,Tweets,Replys,reTweets,Likes)
                    ,columns=['UserTags','TimeStamps','Tweets','Replys','reTweets','Likes'])

    df.head()

    excel_path = "static/data/file.xlsx"  # Update this to your desired path
    df.to_excel(excel_path, index=False)


    df = pd.read_excel(excel_path)
    for _, row in df.iterrows():
        Tweetsdata.objects.create(
            user_tags=row['UserTags'],
            timestamp=row['TimeStamps'],
            tweet=row['Tweets'],
            reply=row['Replys'],
            retweets=row['reTweets'],
            likes=row['Likes']
        )
