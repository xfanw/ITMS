from django.urls import path
from home.views import *
import home.views_account as account

# home url
urlpatterns = [
    path("", home, name="home"),
    path("test", test, name="test"),
]

# account maangement
urlpatterns += [
    path("login", account.itms_login, name="login"),
    path("logout", account.itms_logout, name="logout"),
    path("signup", account.itms_signup, name="signup"),
    path("change_password", account.itms_change_password, name="change_password"),
    path("profile", account.profile, name="profile"),
    # test
]
