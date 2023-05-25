from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# jv0VxLujC1De2xvBzLesnQ==Bj7A0pKc0tunOSpL
# Create your views here.

def Signup(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        



    return render (request,'signup.html')

@login_required(login_url='login')
def about(request):
    # return HttpResponse('Hello world')

    return render(request, 'about.html')

def Login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'Login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    import json
    import requests
    if request.method == 'POST':
        query = request.POST['query']
        api_url = 'https://api.api-ninjas.com/v1/nutrition?query='
        api_request = requests.get(
            api_url + query, headers={'X-Api-Key': 'jv0VxLujC1De2xvBzLesnQ==Bj7A0pKc0tunOSpL'})
        try:
            api = json.loads(api_request.content)
            print(api_request.content)
        except Exception as e:
            api = "oops! There was an error"
            print(e)
        return render(request, 'home.html', {'api': api})
    else:
        return render(request, 'home.html', {'query': 'Enter a valid query'})

def summarize(request):

    return render(request, 'summarize.html')

def speech(request):

    return render(request,'speech.html')

def newsletter(request):

    return render(request, 'newsletter.html')

def email(request):
    
    return render(request, 'email.html')

def audio(request):
    
    return render(request, 'audio.html')

def image(request):
    
    return render(request, 'image.html')

def team(request):
    
    return render(request, 'team.html')
