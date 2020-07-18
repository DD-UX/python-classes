"""
Hacer un programa que tire los dados y calcule el puntaje obtenido para la Generala.

- El usuario solamente va a apretar ENTER para tirar los dados
- Si el usuario ingresa 0, debera mostrar el puntaje final y salir.
- En la generala existe la posibilidad de dejar dados, agarrar otros y seguir jugando. Por ahora solo va a ser una tirada de dados por ronda, y el programa va a elegir a conveniencia que juego conviene marcar. En las reglas se habla de "servida" o "armada", en este caso va a ser siempre servida.
- Si no sale ningun juego el usuario debera elegir cual juego descartar de los que todavia no salieron hasta que no queden juegos disponibles y el programa mostrara los resultados. Ejemplo: Si ya tengo completo los numeros, y no me sale ninguna Escalera/Full/Poker/Generala, se le muestra al usuario cual de esas elegir y se le pone un 0, entonces en la proxima ronda si sale alguno de esos juegos, ya no va a ser valido

Reglas:
-------
Para calcular el puntaje correspondiente a una categoría de números del 1 al 6, se deben sumar los números iguales. Por ejemplo, si un jugador, tirara tres dados con el número 6, se sumará, 6+6+6=18, este resultado se anotará en la casilla correspondiente al número 6. Si son tres 1 se debe anotar 3 al 1, si hay dos 6 se debe anotar 12 al 6.

1: se coloca el número que dé la suma de 1 obtenidos.
2: se coloca el número que dé la suma de 2 obtenidos.
3: se coloca el número que dé la suma de 3 obtenidos.
4: se coloca el número que dé la suma de 4 obtenidos.
5: se coloca el número que dé la suma de 5 obtenidos.
6: se coloca el número que dé la suma de 6 obtenidos.
Escalera: 25 puntos si es servida. Se forma con una progresión de números. Hay tres posibilidades: 1-2-3-4-5 (escalera menor), 2-3-4-5-6 (escalera mayor) o 3-4-5-6-1
Full: 35 puntos si es servido. Se forma con dos grupos de dados iguales, uno de tres y otro de dos dados.
Póker: 45 puntos si es servido. Se forma con cuatro dados iguales.
Generala: 50 puntos si se logra formar cinco números iguales.
"""

from utilities.dado import tirar_dados

juegos = ['Generala', 'Póker', 'Full', 'Escalera', '6', '5', '4', '3', '2', '1']
puntaje = {
    'Generala': None,
    'Póker': None,
    'Full': None,
    'Escalera': None,
    '6': None,
    '5': None,
    '4': None,
    '3': None,
    '2': None,
    '1': None
}

def contar_dados(jugada):
    numeros = {}
    for j in jugada:
        index = str(j)
        if index in numeros:
            numeros[index] += 1
        else:
            numeros[index] = 1
    return numeros


def procesar_juego(jugada):
    data = contar_dados(jugada) # {'1': 3, '6': 1, '5': 1}
    distintos_dados = len(data)
    hizo_juego = False

    # Proceso los juegos no-numéricos
    for juego in filter(lambda x: not x.isdigit() or x is not None, juegos):
        hizo_juego = True

        # Generala
        if juego == 'Generala' and distintos_dados == 1:
            puntaje[juego] = 50
            juegos.remove('Generala')
            break

        # Póker
        elif juego == 'Póker' and distintos_dados == 2:
            primer_valor = list(data.values())[0]
            if primer_valor == 4 or primer_valor == 1:
                puntaje[juego] = 45
                juegos.remove('Póker')
                break

        # Full
        elif juego == 'Full' and distintos_dados == 2:
            primer_valor = list(data.values())[0]
            if primer_valor == 2 or primer_valor == 3:
                puntaje[juego] = 35
                juegos.remove('Full')
                break

        # Escalera
        elif juego == 'Escalera' and distintos_dados == 5 and 3 in jugada:
            puntaje[juego] = 25
            juegos.remove('Escalera')
            break

        # Cuando ninguno aplica, no hizo juego
        else:
            hizo_juego = False

    if not hizo_juego:
        for j, valor in sorted(data.items(), key=lambda kv: kv[1], reverse=True):
            if puntaje[str(j)] is None:
                puntaje[j] = int(j) * valor
                juegos.remove(j)
                hizo_juego = True
                break


    return hizo_juego


def ofrecer_descartar_juego():
    print("===========")
    print("Seleccione un juego para descartar:")
    juegos_disponibles = len(juegos)
    for i in range(juegos_disponibles):
        print("[{}]: {}".format(i + 1, juegos[i]))
    print("[0]: Terminar el juego")
    n = int(input())

    if n > juegos_disponibles:
        ofrecer_descartar_juego()
    else:
        if n < 1:
            print("EXIT!")
        else:
            index = n-1
            puntaje[juegos[index]] = 0
            juegos.remove(juegos[index])


def imprimir_puntaje(mensaje_total='Sub total'):
    for j, valor in puntaje.items():
        if valor == 0:
            valor = '--- Tachada ---'
        elif valor is None:
            valor = 'No hay puntaje'
        print("{}: {}".format(j, valor))

    print("{}: ".format(mensaje_total), sum(filter(lambda x: x is not None, puntaje.values())))


def init():
    for k in juegos[:]:  # Clonar juegos porque va a ir mutando
        accion = input("Presione ENTER para lanzar o 0 para terminar el juego")
        if accion == '0':
            break

        jugada = sorted(tirar_dados())
        hizo_juego = procesar_juego(jugada)

        if not hizo_juego:
            ofrecer_descartar_juego()

        imprimir_puntaje()

    imprimir_puntaje("Total")


init()
