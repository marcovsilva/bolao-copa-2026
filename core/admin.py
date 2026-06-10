from django.contrib import admin
from .models import Group, Team, BracketPrediction, Match, Prediction, Ranking

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'points', 'games_played', 'wins', 'draws', 'losses')
    list_filter = ('group',)

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('team_a', 'team_b', 'stage', 'date', 'score_a', 'score_b')
    list_filter = ('stage', 'date')

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('user', 'match', 'predicted_score_a', 'predicted_score_b', 'points_earned')
    list_filter = ('user',)

@admin.register(Ranking)
class RankingAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_points')
    ordering = ('-total_points',)

@admin.register(BracketPrediction)
class BracketPredictionAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
