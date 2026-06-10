import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bolao_copa.settings')
django.setup()

from django.contrib.auth import get_user_model

def run():
    User = get_user_model()
    # Pega os usuários com este email que não são superusuários (como o adm que você criou)
    users = User.objects.filter(email='marcosvinicius_vini@live.com', is_superuser=False)
    count = users.count()
    if count > 0:
        users.delete()
        print(f"Sucesso: {count} usuário(s) removido(s).")
    else:
        print("Nenhum usuário comum encontrado com esse email para remover.")

if __name__ == '__main__':
    run()
