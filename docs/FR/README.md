# LISEZMOI

- [English version | Version anglaise](https://github.com/seynax/rpg_game?tab=readme-ov-file#readme)

## __Par quoi commencer ?__

  - Cloner les référentiels (où vous voulez)
    > git clone https://github.com/seynax/rpg_game
   
    > clone git https://github.com/seynax/rpg_game_api

  - Lancez l'application flask "game_flask" à partir du dossier rpg_game_api/game
    > cd rpg_game_api/jeu

    - *AVEC MESSAGES DE DÉBOGAGE* :
      > flask --app game_flask exécuter --debug

    - *SANS MESSAGES DE DÉBOGAGE* :
      > flask --app game_flask exécuter

  - Lancer la page web :
    -https://127.0.0.1:5000

  - Exécuter une requête API Rest (GET | POST -> JSON)
    - https://127.0.0.1:5000/api/type/action

  - Lancez le jeu python avec "main.py" depuis rpg_game/
    > cd rpg_game/
    > python3 main.py

## __Comment ça fonctionne ?__
- avec un __Jeu en PYTHON__
- avec un __site WEB et une API__
   - INDEX :
     -https://127.0.0.1:5000
     - https://127.0.0.1:5000/index

   - PAGES :
     - https://127.0.0.1:5000/page

   - FORMULAIRE et REQUÈTES par API :
     - https://127.0.0.1:5000/type/action
     - https://127.0.0.1:5000/api/type/action

     - __Types__ : zone(s), joueur(s)
     - __Actions__ :
       - types : afficher tout
       - types/delete : supprimer plusieurs
       - taper/supprimer : supprimer un
       - types/delete : supprimer plusieurs
       - taper/ajouter : ajouter un

## __Dépôts__ :

- https://github.com/seynax/rpg_game
   - Logique et exécution du jeu
   - Point d'utilisation de l'API
- https://github.com/seynax/rpg_game_api
   - Base de données
   - Vues et formulaires WEB
   - Point de gestion de l'API

## __TODO LIST__

  - https://github.com/seynax/rpg_game/blob/master/docs/TODO.md

## __Qu'est-ce-que ça utilise ?__
- __Langues__
   -Python
   -HTML
- __Bibliothèque et frameworks__
   - Tailwin
   - Flacon
- __API__
   - Repos
- __Paradigme et modèles__
   -Mérise
   - API Reste
- __Conventions__
   - Classe : Nom0Nom1
   - Méthodes, fichier et variables : nom0_nom1
