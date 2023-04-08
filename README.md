# Money Box API application


Application Django de gestion de tirelires et de leurs richesse.
Cette application n'a pas d'interface client mais une API utilisable depuis une documentation Swagger UI.

## Prérequis


Voici les prérequis pour faire fonctionner le serveur de l'application localement:
 - Installer Docker Desktop sur votre machine: https://docs.docker.com/desktop/
 - Pour les machines Windows, veuillez utiliser un terminal où vous pouvez faire marcher des Shell Scripts. Voici un article qui pourrait vous aidez à trouver un outil pour ça: https://www.thewindowsclub.com/how-to-run-sh-or-shell-script-file-in-windows-10

Pour toutes les commandes dans la documentation, veuillez être dans le contexte suivant:
- Veuillez avoir le dépôt Git cloné sur votre machine
- Accéder à l'application depuis un terminal Shell
- Assurez vous que Docker Desktop est démarré

## Construire et faire fonctionner le serveur


Exécuter les commandes suivantes pour construire et démarrer le serveur de l'application:
```console
./scripts/setup-app # Construit les containers et passe les migrations Django
./scripts/start-app # Démarre la base de données Postgres et le serveur Django de l'application
```

## Faire exécuter les test unitaires


Exécuter la commande suivante pour exécuter les test unitaires:
```console
./scripts/run-unit-tests
```

## Utiliser l'API de l'application


Veuillez démarrer le serveur de l'application et dirigez vous sur l'adresse suivante: http://127.0.0.1:8000/moneybox-app/api/swagger-doc/

Vous y retrouvez une documentation Swagger UI, tous les endpoints utilisables par l'application et les détails de chaque actions possibles avec les tirelires seront présents sur cette documentation.

La documentation est intéractive donc vous pouvez créer, lister, retrouver, secouer, épargner et casser des tirelires depuis cet écran.
