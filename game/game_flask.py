import flask
import sqlite3

app = flask.Flask(__name__, template_folder="views")
@app.route('/')
def home():
    connection = sqlite3.connect('../resources/SQLITE/rpg_game.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM stats')
    players_stats = cursor.fetchall()
    connection.close()

    players_stats_list = []

    logs_file = open("logs.log", "w+")
    for player_stat in players_stats:
      logs_file.write(str(player_stat) + "\n")
      players_stats_list.append({
         "player_id":                   player_stat[0],
         "player_name":                 player_stat[1],
         "player_attack":               player_stat[2],
         "player_attack_speed":         player_stat[3],
         "player_defense":              player_stat[4],
         "player_life":                 player_stat[5],
         "player_regeneration_speed":   player_stat[6],
         "player_level":                player_stat[7]
      })
    logs_file.close()
    return flask.render_template('index.html', players_stats_list=players_stats_list)

# Faire un form pour add
@app.route('/add', methods=['GET', 'POST'])
def add():
   if flask.request.method == 'POST':
      parameters = {}
      parameters["name"]               = flask.request.values.get('name')
      parameters["attack"]             = flask.request.values.get('attack')
      parameters["attack_speed"]       = flask.request.values.get('attack_speed')
      parameters["defense"]            = flask.request.values.get('defense')
      parameters["life"]               = flask.request.values.get('life')
      parameters["regeneration_speed"] = flask.request.values.get('regeneration_speed')
      parameters["level"]              = flask.request.values.get('level')

      logs_file = open("logs.log", "w+")
      logs_file.write(str(parameters) + "\n")
      logs_file.close()

      connection = sqlite3.connect('../resources/SQLITE/rpg_game.db')

      cursor = connection.cursor()
      cursor.execute('INSERT INTO stats (player_name, player_attack, player_attack_speed, player_defense, player_life, player_regeneration_speed, player_level) VALUES(:name, :attack, :attack_speed, :defense, :life, :regeneration_speed, :level)',
                     parameters)
      connection.commit()
      connection.close()

      return flask.redirect('/')
   else:
      return flask.render_template('add.html')

@app.route('/Area')
def Area():
   return flask.render_template('Area.html')

@app.route('/delete/<player_id>')
def delete(player_id):
   connection = sqlite3.connect('../resources/SQLITE/rpg_game.db')

   cursor = connection.cursor()
   cursor.execute('DELETE FROM stats WHERE player_id = ' + player_id)
   connection.commit()
   connection.close()

   return flask.redirect('/')