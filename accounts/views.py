from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login, logout


# Create your views here.
# registration

# def register(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         email = request.POST['email']
#         password = request.POST['password']
#         cpassword = request.POST['password1']
#         if password == cpassword:
#             if User.objects.filter(username=username).exists():
#                 messages.info(request, "Username Taken")
#                 return redirect('register')
#             elif User.objects.filter(email=email).exists():
#                 messages.info(request, "email Taken")
#                 return redirect('register')
#             else:
#                 user = User.objects.create_user(username=username, password=password, first_name=first_name,
#                                                 last_name=last_name, email=email)
#                 user.save();
#                 return redirect('login')
#         else:
#             messages.info(request, "password not matching")
#             return redirect('register')
#         return redirect('/')
#     return render(request, "register.html")


def register(request):
    if request.user.is_authenticated:
        return redirect("main:home")

    # if they are not logged in
    else:
        if request.method == "POST":
            form = RegistrationForm(request.POST or None)
            # check if the form is valid
            if form.is_valid():
                user = form.save()

                # get the raw password
                raw_password = form.cleaned_data.get('password1')

                # authenticate the user
                user = authenticate(username=user.username, password=raw_password)

                # login the user
                login(request, user)

                return redirect("main:home")
        else:
            form = RegistrationForm()
        return render(request, "register.html", {"form": form})


#
#
# login
def login_user(request):
    if request.user.is_authenticated:
        return redirect("main:home")
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']

            print(username, password)
            # check the credentials
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("main:home")
                else:
                    return render(request, 'login.html', {"error": "Your account has been disabled."})
            else:
                return render(request, 'login.html', {"error": "Invalid Username or Password. Try Again."})
        return render(request, 'login.html')


# logout user
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        print("Logged out succesfully")
        return redirect("accounts:login")
    else:
        return redirect("accounts:login")
