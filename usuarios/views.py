from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import Perfil

def registro(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Perfil.objects.create(usuario=user)
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "usuarios/registro.html", {"form": form})

















# Create your views here.
