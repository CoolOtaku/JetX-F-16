from src import Const


def process_command(command):
    try:
        parts = command.split()
        action = parts[0].lower()
        if action == 'get':
            variable = parts[1].lower()
            handle_get(variable)
        elif action == 'set':
            variable = parts[1].lower()
            value = parts[2]
            handle_set(variable, value)
        elif action == 'help':
            help_command()
        elif action == 'exit':
            Const.IS_RUNNING = False
        else:
            print('Invalid command')
    except IndexError:
        print('Invalid command')
    except Exception as e:
        print(f'Error: {e}')


def handle_set(variable, value):
    print(f'Setting {variable} to {value}...')

    if variable == 'android_gui':
        Const.ANDROID_GUI = value.lower() == 'true'
    elif variable == 'time':
        try:
            Const.GAME_DURATION = int(value)
        except ValueError:
            print("Invalid value for 'time'. Please enter an integer value.")
    elif variable == 'view_fps':
        Const.VIEW_FPS = value.lower() == 'true'
    elif variable == 'spawn_interval':
        try:
            Const.SPAWN_INTERVAL = int(value)
        except ValueError:
            print("Invalid value for 'spawn_interval'. Please enter an integer value.")


def handle_get(variable):
    print(f'Getting {variable}...')

    value = None
    if variable == 'android_gui':
        value = Const.ANDROID_GUI
    elif variable == 'time':
        value = Const.GAME_DURATION
    elif variable == 'view_fps':
        value = Const.VIEW_FPS
    elif variable == 'spawn_interval':
        value = Const.SPAWN_INTERVAL
    print(f'Value: {value}...')


def help_command():
    print('Available commands:')
    print('get <variable>: Get the value of a variable')
    print('set <variable> <value>: Set the value of a variable')
    print('All example:')
    print('set android_gui True or False')
    print('set time 60')
    print('set view_fps True or False')
    print('set spawn_interval 1000')
