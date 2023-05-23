from flask import Flask, request, render_template
from jinja2 import Environment, FileSystemLoader
from flask import Flask, redirect, url_for, session

from backend import executarSQL, executarSelectSQL
from flask_session import Session
import mariadb
import sys

app = Flask(__name__, static_url_path='/static')
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

try:

    sentenciaSQL = f"""CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(255),
    contrasenya VARCHAR(255)
    );
    """

    executarSQL(sentenciaSQL)

    sentenciaSQL = f"""CREATE TABLE IF NOT EXISTS partidas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    idJugador INT,
    data DATETIME,
    taulell VARCHAR(255),
    torn INT,
    FOREIGN KEY (idJugador) REFERENCES usuarios(id)
    );
    """
    executarSQL(sentenciaSQL)


except mariadb.Error as e:
    print(f"Error conectando a la base de datos: {e}")
    sys.exit(1)


def newGame():
    board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    session["tokens1"] = 1
    session["tokens2"] = 0
    session["board"] = board
    session["playerActive"] = 1
    session["movimients"] = 0


@app.route('/')
def default():
    enviroment = Environment(loader=FileSystemLoader("Template/"))
    template = enviroment.get_template("index.html")
    contingut = template.render()
    return f'{contingut}'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']

        password = request.form['password']
        try:

            sentenciaSQL = f"""SELECT * from usuarios where usuario = '{username}';
               """
            resultados = executarSelectSQL(sentenciaSQL)

            if len(resultados) == 0:
                resultados = '("algoalgoaglo","algoalgoaglo","algoalgoaglo")'

            resultados = ' '.join(str(elemento) for elemento in resultados).replace("(", "").replace(")", "").replace(
                "'", "")
            resultados = [elem.strip() for elem in resultados.split(',')]

            if resultados[1] != username:
                info = {"info": 'Usuario no encontrado'}
                enviroment = Environment(loader=FileSystemLoader("Template/"))
                template = enviroment.get_template("login.html")
                contingut = template.render(info)
                return f'{contingut}'

            if resultados[1] == username and resultados[2] != password:
                info = {"info": 'La contrasenya es incorrecta'}
                enviroment = Environment(loader=FileSystemLoader("Template/"))
                template = enviroment.get_template("login.html")
                contingut = template.render(info)
                return f'{contingut}'

            if resultados[1] == username and resultados[2] == password:
                session["userId"] = resultados[0]
                return game()
        except mariadb.Error:
            sys.exit(1)

    enviroment = Environment(loader=FileSystemLoader("Template/"))
    template = enviroment.get_template("login.html")
    info = ""
    contingut = template.render(info)
    return f'{contingut}'


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:

            sentenciaSQL = f"""SELECT * from usuarios where usuario = '{username}';
        """
            resultados = executarSelectSQL(sentenciaSQL)

        except mariadb.Error:
            sys.exit(1)

        if len(resultados) != 0:
            info = {"info": 'El nombre de usuario ya está en uso. Por favor, elige otro.'}
            enviroment = Environment(loader=FileSystemLoader("Template/"))
            template = enviroment.get_template("register.html")
            contingut = template.render(info)
            return f'{contingut}'
        else:
            try:

                sentenciaSQL = f"""INSERT INTO usuarios
                (usuario, contrasenya)
                VALUES
                ('{username}','{password}');
                """

                executarSQL(sentenciaSQL)

                info = {"info": 'Usuario registrado correctamente'}
                enviroment = Environment(loader=FileSystemLoader("Template/"))
                template = enviroment.get_template("register.html")
                contingut = template.render(info)
                return f'{contingut}'

            except mariadb.Error:
                sys.exit(1)

    enviroment = Environment(loader=FileSystemLoader("Template/"))
    template = enviroment.get_template("register.html")
    info = ""
    contingut = template.render(info)
    return f'{contingut}'


@app.route('/gameMove', methods=['POST', 'GET'])
def gameMove():

    info = {"tokens1": session['tokens1'], "tokens2": session['tokens2'], "board": session["board"]}
    print(info)
    enviroment = Environment(loader=FileSystemLoader("Template/"))
    template = enviroment.get_template("base.html")
    contingut = template.render(info)
    return f'{contingut}'


@app.route('/movement', methods=['POST', 'GET'])
def move():
    position = request.form['position']
    session["board"][int(position) - 1] = session["playerActive"]
    if session["playerActive"] == 1:
        session["playerActive"] = 2
        session["tokens1"] = 0
        session["tokens2"] = 1
    else:
        session["playerActive"] = 1
        session["tokens1"] = 1
        session["tokens2"] = 0

    winer = checkWiner(session["board"], session["playerActive"])
    if winer == 1:
        info = {"info": "¡Felicitats!\n\nHas guanyat la partida, Jugador 2"}
        enviroment = Environment(loader=FileSystemLoader("Template/"))
        template = enviroment.get_template("finalGame.html")
        contingut = template.render(info)
        sentenciaSQL = f"""DELETE FROM partidas
                      where id = {session["idGame"]}
                      """
        executarSQL(sentenciaSQL)
        return f'{contingut}'

    elif winer == 2:
        info = {"info": "¡Felicitats!\n\nHas guanyat la partida, Jugador 1"}
        enviroment = Environment(loader=FileSystemLoader("Template/"))
        template = enviroment.get_template("finalGame.html")
        contingut = template.render(info)
        sentenciaSQL = f"""DELETE FROM partidas
                      where id = {session["idGame"]}
                      """
        executarSQL(sentenciaSQL)
        return f'{contingut}'

    elif winer == 3:
        info = {"info": "Llastima\n\nLa partida ha quedat en empat"}
        enviroment = Environment(loader=FileSystemLoader("Template/"))
        template = enviroment.get_template("finalGame.html")
        contingut = template.render(info)
        sentenciaSQL = f"""DELETE FROM partidas
                      where id = {session["idGame"]}
                      """
        executarSQL(sentenciaSQL)
        return f'{contingut}'

    info = {"tokens1": session['tokens1'], "tokens2": session['tokens2'], "board": session["board"]}
    print(info)
    enviroment = Environment(loader=FileSystemLoader("Template/"))
    template = enviroment.get_template("base.html")
    contingut = template.render(info)
    return f'{contingut}'


@app.route('/game')
def game():
    newGame()
    enviroment = Environment(loader=FileSystemLoader("Template/"))
    template = enviroment.get_template("base.html")
    info = {"tokens1": session['tokens1'], "tokens2": session['tokens2'], "board": session["board"]}
    contingut = template.render(info)
    return f'{contingut}'


def checkWiner(chess, player):
    # COMPROVAR FILES
    if chess[0] == chess[1] == chess[2] != 0:
        return player
    if chess[3] == chess[4] == chess[5] != 0:
        return player
    if chess[6] == chess[7] == chess[8] != 0:
        return player

    # COMPROVAR COLUMNES
    if chess[0] == chess[3] == chess[6] != 0:
        return player
    if chess[1] == chess[4] == chess[7] != 0:
        return player
    if chess[2] == chess[5] == chess[8] != 0:
        return player

    # COMPROVAR COLUMNES
    if chess[0] == chess[4] == chess[8] != 0:
        return player
    if chess[2] == chess[4] == chess[6] != 0:
        return player

    session["movimients"] = session["movimients"] + 1
    print(session["movimients"])
    if session["movimients"] == 9:
        return 3


@app.route('/saveGame')
def saveGame():
    try:
        print(session["userId"])
        sentenciaSQL = f"""INSERT INTO partidas
        (idJugador, data, taulell, torn)
        VALUES
        ({session["userId"]},DATE_FORMAT(NOW(), '%Y-%m-%d %H:%i:%s'),'{session["board"]}',{session["playerActive"]});
        """
        executarSQL(sentenciaSQL)

    except mariadb.Error:
        sys.exit(1)

    return retornaPagina()


def retornaPagina():
    print(session["board"])
    info = {"tokens1": session['tokens1'], "tokens2": session['tokens2'], "board": session["board"]}
    enviroment = Environment(loader=FileSystemLoader("Template/"))
    template = enviroment.get_template("base.html")
    contingut = template.render(info)
    return f'{contingut}'


@app.route('/recoverGame')
def recoverGame():
    registredGames = []
    try:

        sentenciaSQL = f"""SELECT id,DATE_FORMAT(data, '%Y-%m-%d %H:%i:%s'),taulell,torn from partidas where 
        idJugador = '{session["userId"]}' order by data desc;
           """

        resultados = executarSelectSQL(sentenciaSQL)

        for x in resultados:
            registredGames.append(x)

        registredGames = {"registredGames": registredGames}

        enviroment = Environment(loader=FileSystemLoader("Template/"))
        template = enviroment.get_template("recoverGame.html")
        contingut = template.render(registredGames)
        return f'{contingut}'

    except mariadb.Error:
        retornaPagina()
        sys.exit(1)


@app.route('/game/<idGame>')
def choseGame(idGame):
    session["idGame"] = idGame
    try:
        resultatGame = []
        sentenciaSQL = f"""SELECT taulell,torn from partidas where 
              id = '{idGame}';
                 """

        resultados = executarSelectSQL(sentenciaSQL)

        session["board"] = resultados[0][0].replace("[", "").replace("]", "").replace(",", "")

        for i in session["board"].split():
            resultatGame.append(int(i))

        session['board'] = resultatGame
        if resultados[0][1] == 1:
            session['tokens1'] = 1
            session['tokens2'] = 0
            session["playerActive"] = 1
        else:
            session['tokens1'] = 0
            session['tokens2'] = 1
            session["playerActive"] = 2

        return redirect(url_for('gameMove'))

    except mariadb.Error:
        retornaPagina()
        sys.exit(1)
