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

Primer és té que indicar en la variable conn, les dades de la que utilitzarem
```
 conn = mariadb.connect(
            user="nom del Usuari",
            password="contrasenya",
            host="host",
            port=port,
            database="base de dades a utilitzar"
        )
  ```
Posteriorment en el cas del SELECT amb les següents comandes executem el SELECT i ens torna el resultat en la variable resultat i posteriorment fiquem un retorn per tornar la informació. 
```
    cur = conn.cursor()
    cur.execute(sentencia)
    conn.commit()
    resultat = cur.fetchall()
    conn.close()
        return resultat
  ```

En tots els altres casos, executem la comanda i es farà l'acció.
```
    cur = conn.cursor()
    cur.execute(sentencia)
    conn.commit()

    conn.close()
  ```
En tots dos casos al final sempre hem de tancar la consulta per tal de no provocar errors amb:
``` sh
    conn.close()
  ```
Com ja s'ha vist anteriorment.

Teniu tot el compnent de mariaDB a [backend.py](backend.py)