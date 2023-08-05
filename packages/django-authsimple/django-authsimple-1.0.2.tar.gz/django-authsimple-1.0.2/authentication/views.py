from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .helper import send_mail
from .models import Verifiaction, ForgotPassword
from simpleAuth import *
# Create your views here.


def verification_link(user, email):
    v = Verifiaction.objects.create(user_id=user.id)
    domain = DOMAIN
    send_mail(email, "VERIFY EMIAL",
              f"Please verify email <a href={domain}/auth/verify/{v.code}>here</a>.")


def forgot_password_link(user, email):
    v = ForgotPassword.objects.create(user_id=user.id)
    domain = DOMAIN
    send_mail(email, "RESET PASSWORD LINK",
              f"Click <a href={domain}/auth/reset_password/{v.code}>here</a> to reset password.")


def register(request):
    if request.method == 'POST':
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            User.objects.get(username=email)
            return render(request, 'authentication/invalid.html', {
                'message': 'Email is already used. <a href="/auth/forgot_password/"> Forgot Password?? </a>'
            })
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=email, email=email, password=password)

        verification_link(user, email)

        return render(request, 'authentication/success.html', {
            'message': 'Registered SuccesFully !!'
        })

    return render(request, 'authentication/register.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(request, username=email, password=password)

        if user is not None:
            try:
                Verifiaction.objects.get(user_id=user.id)
                return render(request, 'authentication/invalid.html', {
                    'message': 'Please complete email varification. <a href="/auth/verify/new/">Resend verification Link</a>'
                })
            except Verifiaction.DoesNotExist:
                login(request, user)
                return HttpResponseRedirect("/")
        else:
            return render(request, "authentication/invalid.html", {
                'message': 'Invalid Credentials..'
            })

    return render(request, 'authentication/login.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")


def verify(request, code):
    try:
        user_id = Verifiaction.objects.get(code=code).user_id
        Verifiaction.objects.filter(user_id=user_id).delete()
        return HttpResponseRedirect("/auth/login/")
    except Verifiaction.DoesNotExist:
        return render(request, "authentication/invalid.html", {
            'message': 'Code is already used or invalid code',
        })


def verify_new(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(username=email)
            verification_link(user, email)
            return render(request, 'authentication/success.html', {
                'message': 'Link sent to your mailbox !!'
            })
        except User.DoesNotExist:
            return render(request, 'authentication/invalid.html', {
                'message': 'Email is invalid'
            })
    return render(request, 'authentication/newverify.html')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(username=email)
            forgot_password_link(user, email)
            return render(request, 'authentication/success.html', {
                'message': 'Link sent to your mailbox !!'
            })
        except User.DoesNotExist:
            return render(request, 'authentication/invalid.html', {
                'message': 'Email is invalid'
            })
    return render(request, "authentication/forgot_password.html")


def reset_password(request, code):
    try:
        user_id = ForgotPassword.objects.get(code=code).user_id
    except ForgotPassword.DoesNotExist:
        return render(request, "authentication/invalid.html", {
            'message': 'Token is already used or invalid Token',
        })
    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        password = request.POST['password']
        user.set_password(password)
        user.save()

        ForgotPassword.objects.filter(user_id=user.id).delete()
        return HttpResponseRedirect('/auth/login/')

    return render(request, "authentication/reset_password.html", {
        'email': user.email
    })
