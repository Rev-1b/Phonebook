from languages import eng_lang, get_lang_codes, registered_languages
from validators import *

import pandas as pd
import tabulate as tab

pd.set_option('display.max_columns', None)
paginate_by = 5


def set_lang_handler() -> dict[str, str]:
    message = (f'Good afternoon!\n'
               f'Before you start, select your interface language: {", ".join(get_lang_codes())} ... ')
    lang_code = validate_command_input(message=message, options=get_lang_codes(), lang_dict=eng_lang)

    return registered_languages.get(lang_code.upper())


def start_handler(lang_dict: dict[str, str]) -> None:
    message = get_lang_val(key='start', lang_dict=lang_dict)
    show_tutorial = validate_command_input(message=message, options=['y', 'n'], lang_dict=lang_dict)
    if show_tutorial == 'y':
        show_tutorial_handler(lang_dict=lang_dict)


def exit_handler(lang_dict: dict[str, str]) -> None:
    print(get_lang_val('exit_message', lang_dict))
    exit()


def show_tutorial_handler(lang_dict: dict[str, str]) -> None:
    tutorial_steps = ('short_description', 'show_page', 'add_note', 'find_notes', 'change_notes',)

    for step in tutorial_steps:
        message = get_lang_val(key=step, lang_dict=lang_dict)
        further = validate_command_input(message=message, options=['y', 'n'], lang_dict=lang_dict)

        if further == 'n':
            break


def choose_command_handler(lang_dict: dict[str, str]) -> None:
    message = get_lang_val(key='require_input', lang_dict=lang_dict).format(commands=', '.join(commands.keys()))
    command = validate_command_input(message=message, options=commands.keys(), lang_dict=lang_dict)
    commands[command](lang_dict=lang_dict)


def show_page_handler(lang_dict: dict[str, str]) -> None:
    print(get_lang_val(key='chosen_show_list', lang_dict=lang_dict))
    df = pd.read_csv('database.csv', index_col='pk')
    further = True

    while further:
        page = validate_show_input(len(df) // paginate_by + 1, lang_dict)
        if page is None:
            further = False
        else:
            offset = paginate_by * (page - 1)
            print('\n' + tab.tabulate(df[offset:offset + paginate_by]), end='\n\n')


def add_note_handler(lang_dict: dict[str, str]) -> None:
    print(get_lang_val(key='chosen_add_note', lang_dict=lang_dict))
    person = {}

    for field, field_name in database_fields.items():
        message = get_lang_val(key='input_note_data', lang_dict=lang_dict).format(field_name=field_name)
        field_value = validate_data_input(message=message, field=field, lang_dict=lang_dict)
        person[field] = field_value

    df = pd.read_csv('database.csv', index_col='pk')
    df.loc[len(df.index)] = person.values()

    print(get_lang_val(key='note_add_success', lang_dict=lang_dict))
    print(tab.tabulate(df.tail(1)), end='\n\n')

    df.to_csv('database.csv')


def find_notes_handler(lang_dict: dict[str, str]) -> None:
    print(get_lang_val(key='chosen_find_notes', lang_dict=lang_dict))
    query = _get_query(lang_dict)

    df = pd.read_csv('database.csv')
    if len(df) == 0:
        print(get_lang_val('bad_query', lang_dict))
    else:
        print(tab.tabulate(df.loc[df.query(query).index]))


def change_notes_handler(lang_dict: dict[str, str]) -> None:
    print(get_lang_val(key='chosen_find_notes', lang_dict=lang_dict))
    query = _get_query(lang_dict)

    df = pd.read_csv('database.csv', index_col='pk')

    temp_df = df.loc[df.query(query).index]
    if len(temp_df) == 0:
        print(get_lang_val('bad_query', lang_dict))
    else:
        print(tab.tabulate(temp_df.tail(5)))

        new_fields = validate_change_input(database_fields, lang_dict)

        df.loc[df.query(query).index, new_fields.keys()] = tuple(new_fields.values())

        df.to_csv('database.csv')


def _get_query(lang_dict: dict[str, str]) -> tuple[str]:
    queries = []
    further = 'y'

    while further == 'y':
        query = validate_query_input(allowed_query_operations, lang_dict)
        queries.append(query)

        message = get_lang_val(key='add_query', lang_dict=lang_dict)
        further = validate_command_input(message=message, options=['y', 'n'], lang_dict=lang_dict)

    union_query = f'({") & (".join(queries)})'
    return union_query


database_fields = {
    'last_name': 'Фамилия',
    'first_name': 'Имя',
    'middle_name': 'Отчество',
    'organisation': 'Имя Организации',
    'official_number': 'Рабочий номер',
    'personal_number': 'Личный номер',
}

# At the moment, filtering fields is only available by the equal sign, however,
# to add new operations it is enough to register them in this dictionary
allowed_query_operations = {
    'last_name': ('==',),
    'first_name': ('==',),
    'middle_name': ('==',),
    'organisation': ('==',),
    'official_number': ('==',),
    'personal_number': ('==',),
}

commands = {
    'help': show_tutorial_handler,
    'add_note': add_note_handler,
    'show_page': show_page_handler,
    'find_notes': find_notes_handler,
    'change_notes': change_notes_handler,
    'exit': exit_handler,
}
