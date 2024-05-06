from django.shortcuts import render
from login_app.forms import UserForm, UserInfoForm
from login_app.models import UserInfo
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User



def index(request):
    context = {}
    if request.user.is_authenticated:
        current_user = request.user
        user_id = current_user.id
        user_basic_info = User.objects.get(pk=user_id)
        user_more_info = UserInfo.objects.get(user__pk=user_id)
        context = {'user_basic_info': user_basic_info, 'user_more_info': user_more_info}

    return render(request, 'login_app/index.html', context=context)


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        user_info = UserInfoForm(data=request.POST)

        if user_form.is_valid() and user_info.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            user_data = user_info.save(commit=False)
            user_data.user = user

            if 'profile_pic' in request.FILES:
                user_data.profile_pic = request.FILES['profile_pic']
            
            user_data.save()
            registered = True

    else:
        user_form = UserForm()
        user_info = UserInfoForm()

    context = {'user_form': user_form, 'user_info': user_info, 'registered': registered}
    return render(request, 'login_app/register.html', context=context)


# def login_page(request):
#     return render(request, 'login_app/login.html', context={})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('login_app:index'))
                # return render(request, 'login_app/index.html', context={})  # will not change url '/login'
                # return index(request)   # will not change url '/login'
            else:
                return HttpResponse("Account is not active!!")
        else:
            return HttpResponse("Login details are wrong!!")
    else:
        return render(request, 'login_app/login.html', context={})
        # return HttpResponseRedirect(reverse('login_app:login'))


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login_app:index'))
