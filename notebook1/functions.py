from classes import Note, synk, save, load
from decorator import input_error

"""*****************основна логіка роботи та функції*****************"""

"""*******вітання та відповідь на помилкові команди********"""


@input_error
def hello(a):
    return 'How can I help you?'


def wrong_command():
    return 'Wrong command('


def show_all(a):
    synk()
    df = load()
    return df


"""*******парсер введеного тексту з обробкою********"""


@input_error
def parser_string(u_input):
    command, *args = u_input.split()
    if args:
        if ((command + ' ' + args[0]).lower()) in ['show all', 'good bye']:
            command = (command + ' ' + args[0]).lower()
        handler = OPTIONS.get(command.lower(), wrong_command)
    else:
        handler = OPTIONS.get(command.lower(), wrong_command)
    return handler, args


@input_error
def add_note(args):
    df = load()
    name = str(args[0])
    if df['name'].isin([name]).any():
        raise FileExistsError
    else:
        ex_note = Note(name)
        ex_note.add_note()
        save()
    return f'{ex_note.name.value} added'


@input_error
def change_note(args):
    synk()
    df = load()
    name = str(args[0])
    if df['name'].isin([name]).any() == False:
        raise FileNotFoundError
    else:
        ex_note = Note(name)
        ex_note.change_note()
        save()
        return f'{ex_note.name.value} changed'


@input_error
def remove_note(args):
    df = load()
    name = args[0]
    if df['name'].isin([name]).any() == False:
        raise FileNotFoundError
    else:
        ex_note = Note(name)
        df = ex_note.remove()
        save()
        return f'{ex_note.name.value} removed'


@input_error
def add_tags(args):
    df = load()
    name = args[0]
    if df['name'].isin([name]).any():
        ex_note = Note(name)
        tags = input('Enter tags ')
        ex_note.add_tags(tags)
        save()
    else:
        raise FileNotFoundError
    return f'added tags to {ex_note.name.value} '


@input_error
def remove_tags(args):
    df = load()
    name = args[0]
    if df['name'].isin([name]).any():
        ex_note = Note(name)
        ex_note.delete_tags()
        save()
    else:
        raise FileNotFoundError
    return f'removed tags to {ex_note.name.value} '


@input_error
def filter(args):
    df = load()
    tag = args[0]
    # df_filtered=df[df.tags.str.contains(tag, na=False).any()]
    df_filtered = df[df.tags.str.contains('|'.join(tag), na=False)]
    print(df_filtered)


@input_error
def sort(a):
    df = load()
    flag = int(input('Input 1 for sort by date of creation or 2 - by date of change '))
    if flag == 1:
        df_sorted = df.sort_values(by='created', ascending=False)
    else:
        df_sorted = df.sort_values(by='changed', ascending=False)
    print(df_sorted)


OPTIONS = {"hello": hello,
           "add": add_note,
           'change': change_note,
           'delete': remove_note,
           'remove': remove_note,
           'show all': show_all,
           "tag_add": add_tags,
           'tag_delete': remove_tags,
           'tag_remove': remove_tags,
           'filter': filter,
           'sort': sort,
           'good bye': exit,
           'close': exit,
           'exit': exit,
           '.': exit
           }
