from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from .models import Gossip, Comment, SecretPasword, VerySecretPassword
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from django.contrib import messages

import time, logging

logger = logging.getLogger(__name__)

#--------FLAW (2) Cryptographic failures

FIX_2_ENABLED = False

@login_required
def very_secret_gossip(request):
    password, created = SecretPasword.objects.get_or_create(password="secret")
    if request.method == "POST" and request.POST.get("password") == password.password:
        return render(request, "gossip_app/very_secret_gossip_space.html")

#HERE IS THE FIX (5) Security Logging and Monitoring Failures.
    # else:
    #     logger.warning("Failed Secret Gossip access attempt by: %s", request.user.username)
#----------END OF FIX (5)---------------- (FLAW STATE IS JUST TO COMMENT THIS OUT)

    return HttpResponse("<script>alert('Wrong password'); history.back();</script>")
#-----------END OF FLAW (2)------------------

# ----------------FIX FOR FLAW (2)-------------
# FIX_2_ENABLED = True

# @login_required
# def very_secret_gossip(request):
#     try:
#         stored_secret_password = VerySecretPassword.objects.get(
#             user=request.user
#         )
#     except VerySecretPassword.DoesNotExist:
#         return HttpResponse(
#             "<script>alert('You need to set your Secret Gossip password first.'); history.back();</script>"
#         )

#     if request.method == "POST" and check_password(
#         request.POST.get("password"),
#         stored_secret_password.password
#     ):
#         return render(
#             request,
#             "gossip_app/very_secret_gossip_space.html"
#         )
#     #         #HERE IS THE FIX (5)Security Logging and Monitoring Failures.
#     # logger.warning("Failed Secret Gossip access attempt by: %s", request.user.username)
# # #----------END OF FIX (5)---------------- (FLAW STATE IS JUST TO COMMENT THIS OUT)

#     return HttpResponse(
#         "<script>alert('Wrong password'); history.back();</script>"
#     )
#-----END OF FIX (2) CRYPTOGRAPHIC FAILURES


@login_required
def set_secret_password(request):
    if request.method == "POST":
        password = request.POST.get("password")

        VerySecretPassword.objects.update_or_create(
            user=request.user,
            defaults={
                "password": make_password(password)
            }
        )
        messages.success(
            request,
            "Your Very Secret Gossip password has been saved!"
        )
    return redirect(
        "your_account",
        username=request.user.username
    )
        

@login_required
def gossip_list(request):
    gossip_girl, created = User.objects.get_or_create(
        username="gossip_girl"
    )

    Gossip.objects.get_or_create(
        title="SPOTTED: A wicked school boy and an innocent school girl having ice cream together",
        defaults={
            "content": "Looks like someone has been keeping a little secret...",
            "author": gossip_girl
        }
    )
    new_user, _,  =User.objects.get_or_create(
        username="new_user"
    )

    Gossip.objects.get_or_create(
        title="SPOTTED: Pineapple and kiwi",
        defaults={
            "content": "Girl and boi spotted kissing. But who would blame them?",
            "author": new_user
        }
    )
    gossips = Gossip.objects.all()


    #--------------FLAW (3): INJECTION--------
    for gossip in gossips:
        gossip.content = mark_safe(gossip.content)

    #------------END OF FLAW (3)--------------
    #Fix (3): Just comment out the loop for flaw (3)
    return render(
        request,
        "gossip_app/gossip_list.html",
        {"gossips": gossips})

@login_required
def create_gossip(request):
    if request.method == "POST" or request.method == "GET":
        title = request.POST.get("title")
        content = request.POST.get("content")

        if title and content:
            Gossip.objects.create(
                    title=title,
                    content=content,
                    author=request.user
                )

    return redirect("gossip_list")
#HERE IS THE FLAW (1).BROKEN ACCESS CONTROL. Changes to the your_account view and index:
@login_required
def your_account(request, username):
    user = User.objects.get(username=username)

    #-------FIX FOR FLAW (5)
    # if username != request.user.username:
    #     logger.warning(
    #         "Access control failure: user %s attempted to access account %s",
    #         request.user.username,
    #         username
    #     )
    #----- END OF FLIX (5) --- TO HAVE FLAW STATE JUST UNCOMMENT FIX
    gossips = Gossip.objects.filter(
        author=user
    )
    if "login_time" not in request.session:
        request.session["login_time"] = time.time()

    seconds_logged_in = int(
        time.time() - request.session["login_time"]
    )

    return render(
        request,
        "gossip_app/your_account.html",
        {"gossips": gossips, 
         "seconds_logged_in": seconds_logged_in,
         "fix_2_enabled": FIX_2_ENABLED,}
    )

def index(request):
    if not User.objects.filter(username="gossip_girl").exists():
        User.objects.create_user(
            username="gossip_girl",
            password="testpassword123"
        )
    if not User.objects.filter(username="bob").exists():
        User.objects.create_user(
            username="bob",
            password="squarepants"
        )
    if not User.objects.filter(username="alice").exists():
        User.objects.create_user(
            username="alice",
            password="redqueen"
        )
    if request.user.is_authenticated:
        return redirect(
            "your_account",
            username=request.user.username
        )

    return render(request, "gossip_app/index.html")
#-------END OF FLAW (1)--------

#FIX (1) BROKEN ACCESS CONTROL
# @login_required
# def your_account(request, username):
# #------------- FIX (5) SECURITY LOGGING AND MONITORING FAILURES
#     # if username != request.user.username:
#     #     logger.warning(
#     #         "Access control failure: user %s attempted to access account %s",
#     #         request.user.username,
#     #         username
#     #     )
# #END OF FIX (5) -- TO HAVE THE FLAW, JUST COMMENT THIS OUT
#     gossips = Gossip.objects.filter(author=request.user)

#     if "login_time" not in request.session:
#         request.session["login_time"] = time.time()

#     seconds_logged_in = int(
#         time.time() - request.session["login_time"]
#     )
#     return render(request, "gossip_app/your_account.html", {"gossips": gossips, "seconds_logged_in": seconds_logged_in})

# def index(request):
#     if request.user.is_authenticated:
#         return redirect(
#             "your_account",  username=request.user.username)
#     return render(request, "gossip_app/index.html")
#---END OF FIX (1)


def register(request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
        else:
            form = UserCreationForm()
        return render(request, "gossip_app/register.html", {"form": form})
