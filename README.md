# README

- [Version française | French version](https://github.com/seynax/rpg_game/blob/master/docs/FR/README.md)

## __Getting started__

 - Clone repositories (where you want)
   > git clone https://github.com/seynax/rpg_game
   
   > git clone https://github.com/seynax/rpg_game_api

 - Launch game_flask flask application from rpg_game_api/game folder
   > cd rpg_game_api/game

   - *WITH DEBUG LOGS* :
     > flask --app game_flask run --debug

   - *WITHOUT DEBUG LOGS* :
     > flask --app game_flask run

 - Launch web page :
   - https://127.0.0.1:5000

 - Execute API request (GET | POST -> JSON)
   - https://127.0.0.1:5000/api/type/action

 - Launch python game with main.py from rpg_game/
   > cd rpg_game/
   > python3 main.py

## __How work ?__
- with __PYTHON Game__
- with __WEB and API__
  - HOME :
    - https://127.0.0.1:5000
    - https://127.0.0.1:5000/index

  - PAGES :
    - https://127.0.0.1:5000/page

  - FORM and API REQUEST :
    - https://127.0.0.1:5000/type/action
    - https://127.0.0.1:5000/api/type/action

    - __Types__ : area(s), player(s)
    - __Actions__ :
      - types               : show all
      - types/delete : delete multiples
      - type/delete   : delete one
      - types/delete : delete multiples
      - type/add        : add one

## __Repositories__ :

- https://github.com/seynax/rpg_game
  - Game logics and execution
  - API use point
- https://github.com/seynax/rpg_game_api
  - Database
  - WEB views and forms
  - API manage point

## __TODO LIST__

 - https://github.com/seynax/rpg_game/blob/master/docs/TODO.md

## __What is used ?__
- __Languages__
  - Python
  - HTML
- __Library and frameworks__
  - Tailwin
  - Flask
- __API__
  - Rest
- __Paradigm and patterns__
  - Merise
  - API Rest
- __Conventions__
  - Class : Name0Name1
  - Methods, file and variables : name0_name1
