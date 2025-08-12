from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, transaction
from django.contrib import messages
# Create your views here.


def home_view(request:HttpRequest):

    return render(request, 'main/index.html' )


def sign_up(request: HttpRequest):

    if request.method == "POST":

        try:
            with transaction.atomic():
                new_user = User.objects.create_user(username=request.POST["username"],password=request.POST["password"],email=request.POST["email"], first_name=request.POST["first_name"], last_name=request.POST["last_name"])
                new_user.save()

            messages.success(request, "Registered User Successfuly", "alert-success")
            return redirect('management:product_list')
        
        except IntegrityError as e:
            messages.error(request, "Please choose another username", "alert-danger")
        except Exception as e:
            messages.error(request, f"Couldn't register user. Try again {e}", "alert-danger")
            print(e)
    

    return render(request, "main/index.html")



def sign_in(request:HttpRequest):

    if request.method == "POST":

        #checking user credentials
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        print(user)
        if user:
            #login the user
            login(request, user)
            messages.success(request, "Logged in successfully", "alert-success")
            return redirect('management:product_list')
        else:
            messages.error(request, "Please try again. You credentials are wrong", "alert-danger")



    return render(request, "main/index.html")



def log_out(request: HttpRequest):

    logout(request)
    messages.success(request, "logged out successfully", "alert-warning")

    return redirect("main:home_view")
