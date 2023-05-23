import sys

import mariadb


def executarSQL(sentencia):
    try:
        conn = mariadb.connect(
            user="pythonMaster",
            password="Admin1234",
            host="localhost",
            port=3306,
            database="tictactocDB"
        )
    except mariadb.Error as e:
        print(f"Error conectando a la base de datos: {e}")
        sys.exit(1)
    cur = conn.cursor()
    cur.execute(sentencia)
    conn.commit()

    conn.close()


def executarSelectSQL(sentencia):
    try:
        conn = mariadb.connect(
            user="pythonMaster",
            password="Admin1234",
            host="localhost",
            port=3306,
            database="tictactocDB"
        )
    except mariadb.Error as e:
        print(f"Error conectando a la base de datos: {e}")
        sys.exit(1)
    cur = conn.cursor()
    cur.execute(sentencia)
    conn.commit()
    resultat = cur.fetchall()
    conn.close()
    return resultat
