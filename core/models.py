from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class Group(models.Model):
    name = models.CharField(max_length=1)  # A, B, C... L
    
    def __str__(self):
        return f"Grupo {self.name}"

class Team(models.Model):
    name = models.CharField(max_length=100)
    flag_code = models.CharField(max_length=2, help_text="Código ISO da bandeira")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='teams')
    
    points = models.IntegerField(default=0)
    games_played = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    goals_for = models.IntegerField(default=0)
    goals_against = models.IntegerField(default=0)
    
    @property
    def goal_difference(self):
        return self.goals_for - self.goals_against
        
    def recalculate_stats(self):
        matches_a = self.matches_as_a.filter(stage='GR', score_a__isnull=False, score_b__isnull=False)
        matches_b = self.matches_as_b.filter(stage='GR', score_a__isnull=False, score_b__isnull=False)
        
        self.games_played = matches_a.count() + matches_b.count()
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.goals_for = 0
        self.goals_against = 0
        self.points = 0
        
        for m in matches_a:
            self.goals_for += m.score_a
            self.goals_against += m.score_b
            if m.score_a > m.score_b:
                self.wins += 1
                self.points += 3
            elif m.score_a == m.score_b:
                self.draws += 1
                self.points += 1
            else:
                self.losses += 1
                
        for m in matches_b:
            self.goals_for += m.score_b
            self.goals_against += m.score_a
            if m.score_b > m.score_a:
                self.wins += 1
                self.points += 3
            elif m.score_b == m.score_a:
                self.draws += 1
                self.points += 1
            else:
                self.losses += 1
                
        self.save()

    def __str__(self):
        return self.name

class BracketPrediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bracket_predictions')
    created_at = models.DateTimeField(auto_now_add=True)
    bracket_data = models.JSONField(default=dict)
    
    def __str__(self):
        return f"Palpite de {self.user.username} em {self.created_at.strftime('%d/%m/%Y %H:%M')}"

class Match(models.Model):
    STAGE_CHOICES = [
        ('GR', 'Fase de Grupos'),
        ('R32', '16 avos de final'),
        ('R16', 'Oitavas de final'),
        ('QF', 'Quartas de final'),
        ('SF', 'Semifinal'),
        ('FI', 'Final')
    ]
    
    team_a = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_as_a', null=True, blank=True)
    team_b = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_as_b', null=True, blank=True)
    stage = models.CharField(max_length=3, choices=STAGE_CHOICES, default='GR')
    date = models.DateTimeField()
    
    # Placar real
    score_a = models.IntegerField(null=True, blank=True)
    score_b = models.IntegerField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.score_a is not None and self.score_b is not None:
            # Atualizar palpites
            for pred in self.predictions.all():
                pred.calculate_points(self.score_a, self.score_b)
            
            # Recalcular estatísticas dos times se for fase de grupos
            if self.stage == 'GR':
                if self.team_a:
                    self.team_a.recalculate_stats()
                if self.team_b:
                    self.team_b.recalculate_stats()

    def __str__(self):
        return f"{self.team_a} vs {self.team_b} - {self.get_stage_display()}"

class Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='predictions')
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='predictions')
    
    # Palpite do usuário
    predicted_score_a = models.IntegerField()
    predicted_score_b = models.IntegerField()
    
    points_earned = models.IntegerField(default=0)
    
    def calculate_points(self, real_a, real_b):
        old_points = self.points_earned
        
        if self.predicted_score_a == real_a and self.predicted_score_b == real_b:
            self.points_earned = 5
        elif (self.predicted_score_a > self.predicted_score_b and real_a > real_b) or \
             (self.predicted_score_a < self.predicted_score_b and real_a < real_b) or \
             (self.predicted_score_a == self.predicted_score_b and real_a == real_b):
            self.points_earned = 3
        else:
            self.points_earned = 0
            
        if old_points != self.points_earned:
            self.save()
            # Atualizar ranking do usuário
            ranking, created = Ranking.objects.get_or_create(user=self.user)
            ranking.recalculate_total()

    def __str__(self):
        return f"Palpite de {self.user.email} para {self.match}"

class Ranking(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ranking')
    total_points = models.IntegerField(default=0)
    
    def recalculate_total(self):
        from django.db.models import Sum
        total = self.user.predictions.aggregate(Sum('points_earned'))['points_earned__sum'] or 0
        self.total_points = total
        self.save()

    def __str__(self):
        return f"{self.user.email} - {self.total_points} pontos"
