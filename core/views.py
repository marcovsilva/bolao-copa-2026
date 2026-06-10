from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
import json
import string
import random
from .models import Group, Team, BracketPrediction, Match, Ranking, Prediction

def home(request):
    groups = Group.objects.prefetch_related('teams').all().order_by('name')
    group_data = []
    for g in groups:
        teams = g.teams.all()
        # Fetch matches where both teams are in this group (since it's a group stage match)
        matches = Match.objects.filter(stage='GR', team_a__in=teams, team_b__in=teams).order_by('date')
        group_data.append({
            'group': g,
            'teams': teams,
            'matches': matches
        })
    return render(request, 'home.html', {'groups_data': group_data})

def register(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('password')
        confirmar_senha = request.POST.get('confirm_password')
        
        if User.objects.filter(username=email).exists():
            return render(request, 'register.html', {'error': 'E-mail já cadastrado.'})
            
        if senha != confirmar_senha:
            return render(request, 'register.html', {'error': 'As senhas não coincidem.'})
        
        user = User.objects.create_user(username=email, email=email, password=senha, first_name=nome)
        
        send_mail(
            'Bem-vindo ao Bolão da Copa 2026',
            f'Olá {nome},\n\nSeu cadastro foi realizado com sucesso!\nVocê já pode acessar a plataforma e salvar seus palpites.',
            'nao-responda@bolaocopa.com',
            [email],
            fail_silently=False,
        )
        
        return redirect('login')
        
    return render(request, 'register.html')

@login_required
def meus_palpites(request):
    palpites = BracketPrediction.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'meus_palpites.html', {'palpites': palpites})

@login_required
def view_prediction(request, id):
    try:
        prediction = BracketPrediction.objects.get(id=id, user=request.user)
    except BracketPrediction.DoesNotExist:
        raise Http404("Palpite não encontrado.")
    
    teams = list(Team.objects.values('name', 'flag_code'))
    return render(request, 'view_prediction.html', {
        'prediction': prediction,
        'teams_json': json.dumps(teams),
        'bracket_json': json.dumps(prediction.bracket_data)
    })

@login_required
@csrf_exempt
def save_prediction(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Salvar os placares individuais
            if 'placares' in data:
                for p in data['placares']:
                    if p['score_a'] != '' and p['score_b'] != '':
                        Prediction.objects.update_or_create(
                            user=request.user,
                            match_id=p['match_id'],
                            defaults={
                                'predicted_score_a': int(p['score_a']),
                                'predicted_score_b': int(p['score_b'])
                            }
                        )

            # Salvar o chaveamento do mata-mata
            BracketPrediction.objects.create(
                user=request.user,
                bracket_data=data.get('mataMata', [])
            )
            
            # Garantir que o usuário apareça no ranking (com 0 pontos se ainda não tiver)
            Ranking.objects.get_or_create(user=request.user)
            
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'invalid'}, status=400)

def ranking(request):
    # Garante que usuários antigos que já têm palpites, mas não tinham a tabela Ranking, sejam criados agora com 0 pontos
    from django.contrib.auth.models import User
    users_with_predictions = User.objects.filter(bracket_predictions__isnull=False).distinct()
    for u in users_with_predictions:
        Ranking.objects.get_or_create(user=u)
        
    rankings = Ranking.objects.select_related('user').all().order_by('-total_points')
    return render(request, 'ranking.html', {'rankings': rankings})

from django.contrib import messages

def jogos(request):
    if request.method == 'POST' and request.user.is_superuser:
        for key, value in request.POST.items():
            if key.startswith('score_a_'):
                match_id = key.split('_')[-1]
                score_a = value
                score_b = request.POST.get(f'score_b_{match_id}')
                
                if score_a != "" and score_b != "":
                    try:
                        match = Match.objects.get(id=match_id)
                        # Only update if changed to avoid unnecessary recalculations
                        if match.score_a != int(score_a) or match.score_b != int(score_b):
                            match.score_a = int(score_a)
                            match.score_b = int(score_b)
                            match.save()
                    except Match.DoesNotExist:
                        pass
        messages.success(request, 'Resultados reais atualizados com sucesso! Classificação e Ranking foram recalculados.')
        return redirect('jogos')
        
    matches = Match.objects.select_related('team_a', 'team_b').all().order_by('date')
    return render(request, 'jogos.html', {'matches': matches})
