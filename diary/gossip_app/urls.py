from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login/", auth_views.LoginView.as_view(template_name="gossip_app/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    #FLAW: for (1) Broken Access Control: the url contains user name
    path("your-account/<str:username>/",views.your_account,name="your_account"),
    # FIX for (1) Broken Access Control
    path("your_account/", views.your_account, name="your_account"),
    path("gossips/", views.gossip_list, name="gossip_list"),
    path("gossips/create/", views.create_gossip, name="create_gossip"),
    path("gossip_app/very_secret_gossip_space", views.very_secret_gossip, name="very_secret_gossip")
]