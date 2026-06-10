from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from core.views import home, register, meus_palpites, save_prediction, view_prediction, ranking, jogos

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('cadastro/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('meus-palpites/', meus_palpites, name='meus_palpites'),
    path('meus-palpites/<int:id>/', view_prediction, name='view_prediction'),
    path('salvar-palpite/', save_prediction, name='save_prediction'),
    path('ranking/', ranking, name='ranking'),
    path('jogos/', jogos, name='jogos'),
    
    path('recuperar-senha/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('recuperar-senha/enviado/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('recuperar-senha/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('recuperar-senha/concluido/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]
