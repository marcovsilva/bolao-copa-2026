import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bolao_copa.settings')
django.setup()

from core.models import Group, Team, Match
from django.utils import timezone
from datetime import timedelta

def run():
    # Grupos da Copa 2026 (Com as seleções exatas enviadas)
    groups_data = {
        'A': [('México', 'MX'), ('África do Sul', 'ZA'), ('República da Coreia', 'KR'), ('Tchéquia', 'CZ')],
        'B': [('Canadá', 'CA'), ('Bósnia e Herzegovina', 'BA'), ('Catar', 'QA'), ('Suíça', 'CH')],
        'C': [('Brasil', 'BR'), ('Marrocos', 'MA'), ('Haiti', 'HT'), ('Escócia', 'GB-SCT')],
        'D': [('EUA', 'US'), ('Paraguai', 'PY'), ('Austrália', 'AU'), ('Turquia', 'TR')],
        'E': [('Alemanha', 'DE'), ('Curaçau', 'CW'), ('Costa do Marfim', 'CI'), ('Equador', 'EC')],
        'F': [('Holanda', 'NL'), ('Japão', 'JP'), ('Suécia', 'SE'), ('Tunísia', 'TN')],
        'G': [('Bélgica', 'BE'), ('Egito', 'EG'), ('RI do Irã', 'IR'), ('Nova Zelândia', 'NZ')],
        'H': [('Espanha', 'ES'), ('Cabo Verde', 'CV'), ('Arábia Saudita', 'SA'), ('Uruguai', 'UY')],
        'I': [('França', 'FR'), ('Senegal', 'SN'), ('Iraque', 'IQ'), ('Noruega', 'NO')],
        'J': [('Argentina', 'AR'), ('Argélia', 'DZ'), ('Áustria', 'AT'), ('Jordânia', 'JO')],
        'K': [('Portugal', 'PT'), ('RD do Congo', 'CD'), ('Uzbequistão', 'UZ'), ('Colômbia', 'CO')],
        'L': [('Inglaterra', 'GB-ENG'), ('Croácia', 'HR'), ('Gana', 'GH'), ('Panamá', 'PA')],
    }

    print("Limpando banco de dados...")
    Match.objects.all().delete()
    Team.objects.all().delete()
    Group.objects.all().delete()

    print("Cadastrando grupos, seleções e jogos...")
    base_date = timezone.now() + timedelta(days=30)
    for group_name, teams in groups_data.items():
        g = Group.objects.create(name=group_name)
        created_teams = []
        for team_name, flag in teams:
            created_teams.append(Team.objects.create(name=team_name, flag_code=flag, group=g))
            
        pairs = [(0,1), (2,3), (0,2), (1,3), (0,3), (1,2)]
        for i, (idx1, idx2) in enumerate(pairs):
            Match.objects.create(
                team_a=created_teams[idx1],
                team_b=created_teams[idx2],
                stage='GR',
                date=base_date + timedelta(days=i)
            )

    print("Seed concluído com sucesso!")

if __name__ == '__main__':
    run()

