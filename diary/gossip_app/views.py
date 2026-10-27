from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

@login_required
def gossip_list(request):
     return None

@login_required
def your_account(request):
    return render(request, "gossip_app/your_account.html")


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
