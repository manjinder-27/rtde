from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from docshandler.models import Document
from django.contrib.auth import authenticate,login,logout

def homeView(request):
    if request.user.is_authenticated:
        results = Document.objects.filter(owner=request.user)
        files_list = []
        if results.exists():
            for i in results:
                files_list.append({
                    'name': i.name,
                    'desc': 'Modified At ' + str(i.modified_at),
                    'id': i.uniqID
            })
        homeContext = {
            'userName':str(request.user.get_full_name()),
            'data':files_list
        }
        return render(request,'home.html',context=homeContext)
    else:
        return redirect('login_view')


def loginView(request):
    if request.method == "GET":
        return render(request,'login.html',context={'msg':''})
    else:
        user = authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is not None:
            login(request,user)
            return redirect('home_view')
        else:
            return render(request,'login.html',context={'msg':'Invalid User Credentials'})


def registerView(request):
    if request.method == "GET":
        return render(request,'register.html',context={'msg':''})
    else:
        username = request.POST['username']
        email = request.POST['email']
        passwd1 = request.POST['password1']
        passwd2 = request.POST['password2']
        name = request.POST['name']
        try:
            user = User.objects.get(username=username)
            return render(request,'register.html',context={'msg':'Username already taken by another user , Try another username'})
        except:
            try:
                user = User.objects.get(email=email)
                return render(request,'register.html',context={'msg':'This Email is already used with another account , Use another email'})
            except:
                if passwd1 != passwd2:
                    return render(request,'register.html',context={'msg':'Passwords didn\'t matched'})
                user = User.objects.create_user(username=username,email=email,password=passwd1,first_name=name)
                user.save()
                login(request,user)
                return redirect('home_view')
        
    
def logoutView(request):
    logout(request)
    return redirect('login_view')