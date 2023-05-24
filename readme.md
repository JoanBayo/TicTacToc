## Que és un component?

En programació, un component és una unitat modular i reutilitzable de programari que fa una funció específica dins d'un sistema més gran. Pot ser una part independent o interconnectada d'un programa que encapsula una funcionalitat determinada i pot ser utilitzat per altres components o mòduls per construir una aplicació completa.
Els components es caracteritzen per tenir una interfície ben definida i es poden comunicar amb altres components a través de mètodes, esdeveniments o missatges. El seu objectiu principal és promoure la modularitat, el re-ús i la facilitat de manteniment en el desenvolupament de programari, permetent dividir la lògica del programa en parts més petites i enfocades a tasques específiques.

## MariaDB

En aquest cas s'ha utilitzat mariaDB, MariaDB és un sistema de gestió de bases de dades de codi obert i compatible amb MySQL, que ofereix una alta velocitat, escalabilitat i seguretat per a l'emmagatzematge i la recuperació d'informació.
Es pot treballar amb MariaDB mitjançant el terminal o bé en el mateix Python3-10 instal·lant la següent llibreria.

  ```sh
  pip install mariadb sys
  ```
Com podeu comprovar en el fitxer backend.py, és molt fàcil d'utilitzar, i sol amb aquestes línies de codi podeu fer SELECT, INSERT, CREATE i UPDATE.

## Com funciona el component de MariaDB.

Del nostre component sols haurem d'importar dues funcions al fitxer principal amb el següent import
```
from backend import executarSQL, executarSelectSQL
  ```
Primer és té que indicar en la variable conn, les dades de la que utilitzarem, això es tindra que ficar en el principi de cada funcio del component.
```
conn = mariadb.connect(
        user="nom del Usuari",
        password="contrasenya",
        host="host",
        port=port,
        database="base de dades a utilitzar"
        )
  ```
Per fer un SELECT necessitarem executarSelectSQL i introduir com a variable la sentencia SQL a executar, com en el següent exemple:
```
sentenciaSQL = f"""SELECT id,DATE_FORMAT(data, '%Y-%m-%d %H:%i:%s'),taulell,torn from partidas where 
idJugador = '{session["userId"]}' order by data desc;
   """

resultados = executarSelectSQL(sentenciaSQL)
  ```
Posteriorment s'executra el contingut de dins de la funció, amb les següents comandes executem el SELECT i ens torna el resultat en la variable resultat, fican un retorn obtindrem la informació en el fitxer principal amb el resultats. 
```
cur = conn.cursor()
cur.execute(sentencia)
conn.commit()
resultat = cur.fetchall()
conn.close()

return resultat
```
Per fer qualsevol altra consulta (UPDATE, INSERT, CREATE) necessitarem executarSQL i introduir també com a variable la sentencia SQL a executar
```
sentenciaSQL = f"""CREATE TABLE IF NOT EXISTS usuarios (
id INT AUTO_INCREMENT PRIMARY KEY,
usuario VARCHAR(255),
contrasenya VARCHAR(255)
);
"""
```
```
sentenciaSQL = f"""INSERT INTO usuarios
    (usuario, contrasenya)
    VALUES
    ('{username}','{password}');
    """

    executarSQL(sentenciaSQL)
```
Llavors amb el contingut de la funció s'executara i en aquest cas no retornara res, ja que sol és buscar una acció i no obtenir un resultat.
```
cur = conn.cursor()
cur.execute(sentencia)
conn.commit()

conn.close()
  ```
Teniu tot el compnent de mariaDB a [backend.py](backend.py)