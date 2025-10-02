from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Perfil, Categoria, Despesa
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

@login_required
def principal(request):
    return render(request, "principal.html")

@login_required
def get_perfil(request):
    user = request.user
    perfil, created = Perfil.objects.get_or_create(user=user)
    data = {
        "nome": user.get_full_name() or user.username,
        "foto": perfil.foto or "https://i.pravatar.cc/150",
        "descricao": perfil.descricao or ""
    }
    return JsonResponse(data)

@login_required
@csrf_exempt
def atualizar_perfil(request):
    if request.method == "POST":
        user = request.user
        perfil, created = Perfil.objects.get_or_create(user=user)
        nome = request.POST.get("nome")
        foto = request.POST.get("foto")
        descricao = request.POST.get("descricao")
        senha_antiga = request.POST.get("senha_antiga")
        senha_nova = request.POST.get("senha_nova")

        if not user.check_password(senha_antiga):
            return JsonResponse({"error": "Senha antiga incorreta"}, status=400)

        # Atualiza nome e senha
        user.first_name = nome.split()[0]
        user.last_name = " ".join(nome.split()[1:]) if len(nome.split()) > 1 else ""
        user.set_password(senha_nova)
        user.save()

        # Atualiza perfil
        perfil.foto = foto
        perfil.descricao = descricao
        perfil.save()

        return JsonResponse({"success": True})
    return JsonResponse({"error": "Método inválido"}, status=400)

@login_required
def sair(request):
    logout(request)
    return redirect("/login/")
