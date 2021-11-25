

1)Front(angular) ...front-end-app/web-app$ ng serve
2)back (flask) ...back-end-app/main-app$ flask run
3)reszta backendu ...back-end-app$ sudo docker-compose up

Do debugu można sobie wykomentowac workera z docker-compose i odpalać go z ręki komendą:
python3 app.py
z folderu workera


Docker (wszystko w back-end-app/):

Usunięcie wszystkiego:
sudo docker system prune --all --volumes -f

Budowanie workerów:

sudo docker build ./stockapiworker/ -t stockapiworker:latest --no-cache
sudo docker build ./basicpredworker/ -t basicpredworker:latest --no-cache

jak jakiegos obrazu brakuje i o niego krzyczy to tylko nazwy odpowiednie wstawić:

sudo docker build ./brakujacy_obraz/ -t brakujacy_obraz:latest --no-cache


jeśli docker się wykrzacza na postgresie


http://127.0.0.1:5000/flask/add_company/TSLA
http://127.0.0.1:5000/flask/add_company/RBLX
http://127.0.0.1:5000/flask/add_company/PFE
http://127.0.0.1:5000/flask/add_company/NVDA