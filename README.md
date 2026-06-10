# Bolão Copa do Mundo 2026

Um sistema interativo de bolão da Copa do Mundo de 2026, onde usuários podem se cadastrar, palpitar nos jogos por placar, simular chaves de mata-mata completas, acompanhar os resultados reais e disputar a liderança no ranking oficial.

## Principais Funcionalidades

- **Simulador Interativo do Mata-Mata:** Os usuários preenchem os placares da fase de grupos e o sistema calcula automaticamente a classificação (pontos, vitórias, saldo de gols) e monta de forma dinâmica as chaves do mata-mata (Oitavas, Quartas, Semis e Final).
- **Cadastro Simples:** Cadastro e acesso facilitados, permitindo login diretamente pelo E-mail.
- **Painel Rápido de Resultados Reais:** Uma tela exclusiva para o Administrador onde é possível inserir os placares de vários jogos reais da Copa simultaneamente com apenas um clique de salvamento.
- **Sistema de Pontuação:** Ao salvar os resultados reais, o sistema distribui os pontos (5 pontos para placar exato, 3 pontos para acerto de vencedor/empate) e atualiza o Ranking Global automaticamente.
- **Sincronização com API (Robô de Automação):** Comando backend preparado para se conectar a APIs de futebol e automatizar totalmente a atualização de resultados reais em 2026.

## Tecnologias Utilizadas

- **Backend:** Python 3.10+ / Django
- **Frontend:** HTML5 / JavaScript Vanilla / Tailwind CSS (via CDN)
- **Banco de Dados:** SQLite (padrão) pronto para Postgres

## Como executar o projeto localmente

1. Clone o repositório.
2. Crie um ambiente virtual e ative-o:
   ```bash
   python -m venv venv
   source venv/bin/activate  # (No Windows: venv\Scripts\activate)
   ```
3. Instale o Django:
   ```bash
   pip install django requests
   ```
4. Execute as migrações do banco de dados:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. Popule o banco de dados inicial com as Seleções e Grupos (Seed):
   ```bash
   python seed_db.py
   ```
6. Inicie o servidor:
   ```bash
   python manage.py runserver
   ```

## Acesso e Gerenciamento (Admin)

Para ter acesso aos poderes de administrador no frontend (como a tela de "Resultados Reais" interativa) e ao painel padrão do Django:
1. Crie um superusuário no terminal:
   ```bash
   python manage.py createsuperuser
   ```
2. Acesse o site normalmente, faça o Login usando a conta criada e o menu de Administrador aparecerá na barra superior!

## Automação via API-Football (Copa 2026)

O projeto contém um robô pronto para buscar os resultados reais da Copa de 2026 e dar os pontos aos usuários sem intervenção humana.
Para ativar:
1. Adicione a sua `API_FOOTBALL_KEY` no arquivo `settings.py` (ou via variável de ambiente `.env`).
2. Agende o seguinte comando no seu servidor (via Crontab ou agendador de tarefas) para rodar periodicamente:
   ```bash
   python manage.py sync_matches
   ```
