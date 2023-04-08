# Money Box API application


Application Django de gestion de tirelires et de leurs richesses.
Cette application n'a pas d'interface client mais une API utilisable depuis une documentation Swagger UI.

## Prérequis


Voici les prérequis pour faire fonctionner le serveur de l'application localement:
 - Installer Docker Desktop sur votre machine: https://docs.docker.com/desktop/
 - Pour les machines Windows, veuillez utiliser un terminal où vous pouvez faire marcher des Shell Scripts. Voici un article qui pourrait vous être utile: https://www.thewindowsclub.com/how-to-run-sh-or-shell-script-file-in-windows-10

Pour toutes les commandes dans la documentation, veuillez être dans le contexte suivant:
- Veuillez avoir le dépôt Git cloné sur votre machine
- Accéder à l'application depuis un terminal qui peut exécuter des Shell Scripts
- Assurez vous que Docker Desktop est démarré

## Construire et faire fonctionner le serveur


Exécuter les commandes suivantes pour construire et démarrer le serveur de l'application:
```console
./scripts/setup-app # Construit les containers et passe les migrations Django
./scripts/start-app # Démarre la base de données Postgres et le serveur Django de l'application
```

## Faire exécuter les tests unitaires


Exécuter la commande suivante pour exécuter les tests unitaires:
```console
./scripts/run-unit-tests
```

## Utiliser l'API de l'application


Veuillez démarrer le serveur de l'application et dirigez vous sur l'adresse suivante: http://127.0.0.1:8000/moneybox-app/api/swagger-doc/

Vous y retrouvez une documentation Swagger UI avec tous les endpoints utilisables sur l'application et les détails de chaque actions possibles des tirelires.

La documentation est intéractive donc vous pouvez créer, lister, retrouver, secouer, épargner et casser des tirelires depuis cet écran.
