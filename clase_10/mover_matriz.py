"""
Crear un programa con curses que muestre una matriz de 20x20 con un numero 1 (en una posicion al azar) y el resto en None (que se muestra vacio), mostrar la matriz e ir moviendo el 1 con las flechas:


| | | | | |
| | | | | |
| | | | | |
| | |1| | |
| | | | | |

Apretar flecha derecha:
| | | | | |
| | | | | |
| | | | | |
| | | |1| |
| | | | | |

"""
import curses
from utilities.dado import tirar_dados

ROWS = 20
COLUMNS = ROWS

def generar_tablero(rows, cols):
    tablero = {}
    tablero['matriz'] = []

    inyectoValor = False

    while not inyectoValor:
        for x in range(rows):
            tablero['matriz'].append([])
            for y in range(cols):
                valor = 0
                if not inyectoValor and tirar_dados(1)[0] <= 1:
                    inyectoValor = True
                    valor = 1
                    tablero['x'] = x
                    tablero['y'] = y
                tablero['matriz'][x].append("[{}]".format(valor))

    return tablero


tablero = generar_tablero(ROWS, COLUMNS)

KEY_Q = ord('q')
screen = curses.initscr()  # Creates screen object
curses.curs_set(False)

# print(screen.getmaxyx())

try:
    screen.keypad(True)  # Allow arrows
    screen_x = 0
    screen_y = 0
    new_tx = tablero['x']
    new_ty = tablero['y']

    while True:
        current_tx = new_tx
        current_ty = new_ty
        screen_y = 0 # Reset

        screen.clear()  # Deletes older content
        screen.addstr(screen_y, screen_x, 'Move with Keyboard arrows: [<-] [->] [^] [v] | Quit: [Q]')  # Add text
        screen_y += 2
        for line in tablero['matriz']:
            screen.addstr(screen_y, screen_x, ''.join(line))  # Add text
            screen_y += 1

        # Shows added content
        screen.refresh()

        key = screen.getch()  # Get input char
        if key == KEY_Q:
            break
        if key == curses.KEY_LEFT:
            new_ty -= 1
        elif key == curses.KEY_RIGHT:
            new_ty += 1
        elif key == curses.KEY_UP:
            new_tx -= 1
        elif key == curses.KEY_DOWN:
            new_tx += 1

        if new_ty >= COLUMNS:
            new_ty = COLUMNS - 1
        elif new_ty < 0:
            new_ty = 0
        elif new_tx >= ROWS:
            new_tx = ROWS - 1
        elif new_tx < 0:
            new_tx = 0

        tablero['matriz'][current_tx][current_ty], tablero['matriz'][new_tx][new_ty] = tablero['matriz'][new_tx][new_ty], tablero['matriz'][current_tx][current_ty]
except IndexError:
    print("Alcanzaste el límite del juego")
finally:
    screen.keypad(False)
    curses.nocbreak()
    curses.echo()
    curses.endwin()

