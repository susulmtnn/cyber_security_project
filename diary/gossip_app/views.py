from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Gossip, Comment
from django.contrib.auth.models import User
from django.http import HttpResponse


@login_required
def very_secret_gossip(request):
    if request.method == "POST" and request.POST.get("password") == "secret":
        return render(request, "gossip_app/very_secret_gossip_space.html")
    return HttpResponse(
        "<script>alert('Wrong password'); history.back();</script>"
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

    return render(
        request,
        "gossip_app/gossip_list.html",
        {"gossips": gossips}
    )

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


@login_required
def your_account(request):
    gossips = Gossip.objects.filter(author=request.user)
    return render(request, "gossip_app/your_account.html", {"gossips": gossips})


def index(request):
    return render(request, "gossip_app/index.html")


def register(request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("index")
        else:
            form = UserCreationForm()
        return render(request, "gossip_app/register.html", {"form": form})
