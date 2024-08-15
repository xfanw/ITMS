from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.contrib.auth.models import User


# Create your views here.
@login_required
def home(request):
    return render(request, "home/home.html")


def test(request):
    return render(request, "home/test.html")
