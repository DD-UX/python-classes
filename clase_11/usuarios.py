import os
import curses
import hashlib
from datetime import datetime
from utilities.csv_to_map import csv_to_map
from utilities.map_to_csv_array import map_to_csv_array

"""
Generar un programa que permita cargar nuevos usuarios, modificarlos, listarlos y borrarlos

Cada usuario debera tener los siguientes campos:
- id: Numero autoincremental. Al crear un usuario el programa le asignara un numero y debera guardarlo con ese numero
- nombre
- apellido
- email
- created: Fecha en la que se creo el usuario
- last_updated: Fecha de la ultima vez que se modifico (Nice to have)
- password: Usando un hash (import hashlib; hashlib.md5(password.encode()).hexdigest())

El programa debera mostrar un menu principal con las siguientes opciones:
- Ingresar Usuario:
    - Le va a pedir al usuario que ingrese nombre, apellido, email y password
    - Lo va a guardar en el archivo de usuarios
- Modificar Usuario
    - Se le va a pedir el ID de usuario a modificar, va a mostrar los campos nuevamente (Si el usuario no ingresa un valor para ese campo, NO ACTUALIZARLO)
    - Si el ID ingresado no existe, mostrar el error (sin que slaga el programa)
- Listar usuarios
    - Se levanta el archivo de usuarios, y se muestran todos en una tabla (mejor si lo pueden mostrar bien tabulado y lindo)
- Borrar usuario
    - Se ingresa el ID de que usuario a borrar, se muestan los datos de ese usuario y se pide una confirmacion de si esta seguro que quiere borrar ESE usuario.

Formato del archivo donde se guardan los usuarios: CSV
id,nombre,apellido,email,password
1,pablo,diaz,pablo@diaz.com,fkwr8792834jsdkjfk3454sdf
2,diego,diaz,diego@diaz.com,aslkdjlfn3hui7s7yi7hiw73s
3,andii,diaz,andii@diaz.com,flksjdf;jas;ldfj9832u948d
4,viruu,diaz,viruu@diaz,com,lk2hui4hoiuhsakudfhklsuhk
"""

"""
import hashlib
hashlib.md5(password.encode()).hexdigest() -> '2e80a184267270fc8a50f3f9aef3902e'

from datetime import datetime
datetime.now().isoformat() ->  '2020-07-14T23:52:14.382624'
"""

DB = './users.csv'
screen_line_index = 0
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
options = [
    "== [Welcome to users CRUD system] ==",
    "Please select one of the following options",
    "[A]: Read the list of users",
    "[R]: Read an existing user",
    "[C]: Create a new user",
    "[U]: Update an existing use",
    "[D]: Delete an existing user",
    "[Q]: QUIT"
]

user_props = ['id', 'nombre', 'apellido', 'email', 'created', 'last_updated', 'password']


def connect(mode='r'):
    if not os.path.exists(DB):
        headers = ','.join(user_props)
        db = open(DB, 'w')
        db.write(headers + "\n")
        db.close()

    return open(DB, mode)


def create_id():
    existing_users = read_users()

    if len(existing_users) < 1:
        return 0

    last_id = int(existing_users[-1]['id'])
    return last_id + 1


# Create
def create_user(new_user):
    db_connection = connect('a')
    new_user['id'] = str(create_id())
    formatted_user = ','.join(new_user.values())
    db_connection.write(formatted_user + '\n')
    db_connection.close()
    return new_user


# Read All
def read_users():
    db_connection = connect()
    users_list = csv_to_map(db_connection)
    db_connection.close()
    return users_list


# Read
def read_user(user_id):
    users = read_users()
    user = next((x for x in users if x['id'] == user_id), None)
    return user


# Update
def update_user(updated_user):
    # Get DB list of users
    users = read_users()

    # Merge user changes without loosing reference in collection
    for i in range(len(users)):
        if users[i]['id'] == updated_user['id']:
            users[i].update(updated_user)
            break

    # Get collection of lines formatted for CSV
    users_to_csv = map_to_csv_array(users)

    # Override current DB
    db_connection = connect('w')

    # Set each line in DB
    for line in users_to_csv:
        db_connection.write(line + '\n')

    # Close connexion
    db_connection.close()

    # Return updated user
    return updated_user


# Delete
def delete_user(deleted_user):
    # Get DB list of users
    users = read_users()

    # Filter list (exclude deleting user)
    users = filter(lambda x: x['id'] != deleted_user['id'], users)

    # Get collection of lines formatted for CSV
    users_to_csv = map_to_csv_array(list(users))

    # Override current DB
    db_connection = connect('w')

    # Set each line in DB
    for line in users_to_csv:
        db_connection.write(line + '\n')

    # Close connexion
    db_connection.close()

    # Return updated user
    return deleted_user


# Display options
def display_options(screen):
    for line, opt in enumerate(options):
        screen.addstr(line, 0, opt)
    return


# Handle read users command
def handle_read_users(screen):
    users = read_users()
    lines = len(users)

    if lines < 1:
        screen.addstr(0, 0, 'No users listed in the DB')
    else:
        lines = 0
        screen.addstr(lines, 0, '=== READ ALL USERS ===')

        for line, user in enumerate(users):
            lines += 2
            screen.addstr(lines, 0, '== [{} {}] =='.format(user['nombre'], user['apellido']))

            for index, (key, value) in enumerate(user.items()):
                lines += 1
                screen.addstr(lines, 0, '{}: {}'.format(key, value))

    handle_go_back(screen, lines, False)
    return


# Handle read user command
def handle_read_user(screen):
    user = handle_fetch_user(screen)

    if user is None:
        return

    screen.addstr(0, 0, '=== USER ===')

    for index, (key, value) in enumerate(user.items()):
        screen.addstr(index + 1, 0, '{}: {}'.format(key, value))

    handle_go_back(screen, len(user.keys()))
    return


# Handle create user command
def handle_create_user(screen):
    new_user = {
        user_props[0]: None  # ID
    }
    properties_length = len(user_props)

    for index in range(1, properties_length):
        prop = user_props[index]

        screen.addstr(0, 0, '=== NEW USER ===')
        screen.addstr(1, 0, '[ENTER] next')

        if prop == 'created':
            data = datetime.now().strftime(TIME_FORMAT)
        elif prop == 'last_updated':
            data = new_user['created']
        elif prop == 'password':
            data = screen_input(screen, 3, 0, 'Set "{}" property'.format(prop))
            data = hashlib.md5(data.encode()).hexdigest()
        else:
            data = screen_input(screen, 3, 0, 'Set "{}" property'.format(prop))

        # TODO Validate
        # TODO Display and [confirm] [cancel]
        new_user[prop] = data

    create_user(new_user)

    # Final message
    screen.addstr(0, 0, 'User {} {} was created'.format(new_user['nombre'], new_user['apellido']))
    handle_go_back(screen, 0)
    return


# Handle update user command
def handle_update_user(screen):
    user = handle_fetch_user(screen)

    if user is None:
        return

    properties_length = len(user_props)

    for index in range(1, properties_length):
        prop = user_props[index]

        screen.addstr(0, 0, '=== EDIT USER ===')
        screen.addstr(1, 0, 'Leave blank to keep previous value or type a new one')
        screen.addstr(2, 0, '[ENTER] next')

        if prop == 'created':
            continue
        elif prop == 'last_updated':
            data = datetime.now().strftime(TIME_FORMAT)
        elif prop == 'password':
            data = screen_input(screen, 4, 0, 'Set "{}" property'.format(prop))
            if data != "":
                data = hashlib.md5(data.encode()).hexdigest()
        else:
            data = screen_input(screen, 4, 0, 'Set "{}" property'.format(prop))

        # TODO Validate
        # TODO Display and [confirm] [cancel]
        if data != "":
            user[prop] = data

    # Update user in DB
    update_user(user)

    # Final message
    screen.addstr(0, 0, 'User with ID {} updated'. format(user['id']))
    handle_go_back(screen, 0)
    return


# Handle delete user command
def handle_delete_user(screen):
    user = handle_fetch_user(screen)

    if user is None:
        return

    # Delete user in DB
    delete_user(user)

    # Final message
    screen.addstr(0, 0, 'User with ID {} deleted'.format(user['id']))
    handle_go_back(screen, 0)
    return


# Handle go back message
def handle_go_back(screen, index=0, is_recursive=True):
    index += 2
    if is_recursive:
        screen.addstr(index, 0, '[ENTER] Repeat last action')
        index += 1

    screen.addstr(index, 0, '[<-] Go back to menu')
    return


# Handle fetch user by ID
def handle_fetch_user(screen):
    user_id = screen_input(screen, 0, 0, 'Select a user by ID')
    user = read_user(user_id)

    if user is None:
        screen.addstr(0, 0, 'User id {} not found'.format(user_id))
        handle_go_back(screen)
    return user


# Input information in curses screen
def screen_input(screen, r, c, prompt_string):
    curses.echo()
    screen.addstr(r, c, prompt_string)
    screen.refresh()
    data = screen.getstr(r + 1, c, 20)
    screen.clear()
    return data.decode('utf-8')


# Init program
def init():
    KEY_A = ord('a')
    KEY_R = ord('r')
    KEY_C = ord('c')
    KEY_U = ord('u')
    KEY_D = ord('d')
    KEY_Q = ord('q')
    command = display_options
    app_active = True

    screen = curses.initscr()  # Creates screen object

    try:
        screen.keypad(True)  # Allow arrows

        while app_active:
            screen.clear()  # Deletes older content

            command(screen)  # Execute the command assigned by the user

            # Shows added content
            screen.refresh()

            key = screen.getch()  # Get input char

            if key == KEY_A:  # Read [A]ll
                command = handle_read_users
            elif key == KEY_R:  # [R]ead
                command = handle_read_user
            elif key == KEY_C:  # [C]reate
                command = handle_create_user
            elif key == KEY_U:  # [U]pdate
                command = handle_update_user
            elif key == KEY_D:  # [D]elete
                command = handle_delete_user
            elif key == KEY_Q:  # [Q]uit
                app_active = False
            elif key == curses.KEY_LEFT:  # [<-] Go back to menu
                command = display_options
    except IndexError:
        pass
    finally:
        screen.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    return


init()
