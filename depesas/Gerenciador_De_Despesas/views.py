import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Despesa, Categoria
import google.generativeai as genai
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# ------------------ NOVA VIEW INICIAL ------------------
def Home(request):
    # Se o usuário já estiver logado, vai direto para o painel
    if request.user.is_authenticated:
        return redirect('principal')
    return render(request, 'home.html')
# -------------------------------------------------------

# Login
def Login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        remember = request.POST.get('remember', None)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if not remember:
                request.session.set_expiry(0)
            return redirect('principal')
        else:
            return render(request, 'login.html', {'error': 'Usuário ou senha inválidos'})
    return render(request, 'login.html')

# Cadastro
def CriarConta(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request, 'criar_conta.html', {'error': 'Usuário já existe'})

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return redirect('login')

    return render(request, 'criar_conta.html')

# Principal
@login_required
def Principal(request):
    return render(request, 'principal.html')

# Logout
def LogoutView(request):
    logout(request)
    return redirect('login')

# Inicializar categorias padrão
def inicializar_categorias():
    categorias_padrao = ["Moradia", "Alimentação", "Transporte", "Saúde", "Lazer", "Pessoais"]
    for nome in categorias_padrao:
        Categoria.objects.get_or_create(nome=nome)

# Listar categorias
@login_required
def listar_categorias(request):
    inicializar_categorias()
    categorias = Categoria.objects.all()
    data = [{"id": c.id, "nome": c.nome} for c in categorias]
    return JsonResponse(data, safe=False)

# Adicionar despesa
@login_required
def adicionar_despesa(request):
    if request.method == "POST":
        categoria_id = request.POST.get("categoria")
        titulo = request.POST.get("titulo")
        valor = request.POST.get("valor")
        data = request.POST.get("data")

        categoria = Categoria.objects.get(id=categoria_id)
        Despesa.objects.create(
            titulo=titulo,
            valor=valor,
            data=data,
            categoria=categoria
        )
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "erro"})

# Listar despesas
@login_required
def listar_despesas(request):
    despesas = Despesa.objects.select_related('categoria').all().order_by('-data')
    data = [
        {
            'id': d.id,
            'titulo': d.titulo,
            'valor': float(d.valor),
            'data': d.data.strftime('%Y-%m-%d'),
            'categoria': {'id': d.categoria.id, 'nome': d.categoria.nome}
        }
        for d in despesas
    ]
    return JsonResponse(data, safe=False)

# Excluir despesa
@login_required
def excluir_despesa(request, id):
    try:
        despesa = Despesa.objects.get(id=id)
        despesa.delete()
        return JsonResponse({"status": "ok"})
    except Despesa.DoesNotExist:
        return JsonResponse({"status": "erro"})

# ------------------ CHAT IA ------------------
# Configura a API do Google Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@csrf_exempt
@require_POST
@login_required
def chat_ia(request):
    user_message = request.POST.get("message", "")

    if not user_message:
        return JsonResponse({"response": "Envie uma mensagem para começar."})

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(user_message)
        text_response = response.text
        return JsonResponse({"response": text_response})
    except Exception as e:
        return JsonResponse({"response": f"Erro: {str(e)}"})
