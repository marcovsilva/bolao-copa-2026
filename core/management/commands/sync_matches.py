from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Match, Team
import requests
import json

class Command(BaseCommand):
    help = 'Sincroniza os placares reais dos jogos usando a API-Football.'

    def handle(self, *args, **options):
        # NOTA: O ID da Liga para a Copa do Mundo 2026 precisará ser verificado na documentação da API em 2026.
        # Para fins de exemplo, vamos assumir que o league_id da World Cup seja 1.
        LEAGUE_ID = 1
        SEASON = 2026
        API_KEY = getattr(settings, 'API_FOOTBALL_KEY', '')

        if not API_KEY:
            self.stdout.write(self.style.ERROR('API_FOOTBALL_KEY não está configurada no settings.py ou no .env'))
            return

        url = f"https://v3.football.api-sports.io/fixtures?league={LEAGUE_ID}&season={SEASON}"
        
        headers = {
            'x-apisports-key': API_KEY
        }

        try:
            self.stdout.write('Buscando dados da API...')
            response = requests.get(url, headers=headers)
            data = response.json()
            
            if 'errors' in data and data['errors']:
                self.stdout.write(self.style.ERROR(f"Erro na API: {data['errors']}"))
                return

            fixtures = data.get('response', [])
            updated_count = 0

            for fixture in fixtures:
                # Extraindo dados do jogo da API
                status = fixture['fixture']['status']['short']
                if status in ['FT', 'AET', 'PEN']: # Partida finalizada
                    home_name = fixture['teams']['home']['name']
                    away_name = fixture['teams']['away']['name']
                    
                    home_goals = fixture['goals']['home']
                    away_goals = fixture['goals']['away']

                    # Tentando encontrar a partida no banco local
                    # A busca por nome precisa ser exata ou usar um mapeamento
                    try:
                        team_a = Team.objects.get(name__icontains=home_name)
                        team_b = Team.objects.get(name__icontains=away_name)
                        
                        match = Match.objects.filter(team_a=team_a, team_b=team_b).first()
                        if match and (match.score_a != home_goals or match.score_b != away_goals):
                            match.score_a = home_goals
                            match.score_b = away_goals
                            match.save() # Isso já aciona o cálculo de pontos do sistema
                            updated_count += 1
                            self.stdout.write(self.style.SUCCESS(f'Atualizado: {team_a.name} {home_goals} x {away_goals} {team_b.name}'))
                            
                    except Team.DoesNotExist:
                        # Em produção, um dicionário de tradução (ex: "Brazil" -> "Brasil") seria ideal
                        pass

            self.stdout.write(self.style.SUCCESS(f'Sincronização finalizada! {updated_count} jogos atualizados.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ocorreu um erro: {str(e)}'))
