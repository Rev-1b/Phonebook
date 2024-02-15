from languages import eng_lang, get_lang_codes, registered_languages
from validators import *

import pandas as pd
from tabulate import tabulate

pd.set_option('display.max_columns', None)
paginate_by = 5


def set_lang_handler() -> dict[str, str]:
    message = (f'Good afternoon!\n'
               f'Before you start, select your interface language: {", ".join(get_lang_codes())} ... ')
    lang_code = validate_command_input(message, get_lang_codes(), eng_lang)

    return registered_languages.get(lang_code.upper())


def start_handler(lang_dict: dict[str, str]) -> None:
    message = lang_dict.get('start', '__ERROR__')
    show_tutorial = validate_command_input(message, options=['y', 'n'], lang_dict=lang_dict)
    if show_tutorial == 'y':
        show_tutorial_handler(lang_dict)


def show_tutorial_handler(lang_dict: dict[str, str]) -> None:
    """

    Goes through all training points, the user is given the opportunity
    to exit the training mode at any time.

    """
    tutorial_steps = ('short_description', 'show_page', 'add_note', 'find_notes', 'change_notes',)

    for step in tutorial_steps:
        message = lang_dict.get(step, '__ERROR__')
        further = validate_command_input(message, options=['y', 'n'], lang_dict=lang_dict)

        if further == 'n':
            break


def choose_command_handler(lang_dict: dict[str, str]) -> None:
    """

    Basic function that calls a specific handler depending on the command
    entered by the user.

    """
    message = lang_dict.get('require_input', '__ERROR__').format(commands=', '.join(commands.keys()))
    command = validate_command_input(message, commands.keys(), lang_dict)
    commands[command](lang_dict)


def show_page_handler(lang_dict: dict[str, str]) -> None:
    """

    The function will request and display the page as requested by
    the user until the 'exit' command is received.
    The number of records displayed on an individual page is configured in
    the paginate_by variable.

    """
    print(lang_dict.get('chosen_show_list', '__ERROR__'))
    df = pd.read_csv('database.csv', index_col='pk')
    further = True

    if len(df) == 0:
        print(lang_dict.get('empty_table', '__ERROR__'))
        return

    while further:
        page = validate_show_input((max(1, len(df)) - 1) // paginate_by + 1, lang_dict)
        if page is None:
            further = False
        else:
            offset = paginate_by * (page - 1)
            print('\n' + tabulate(df[offset:offset + paginate_by], headers=['ID', *database_fields.values()]),
                  end='\n\n')


def add_note_handler(lang_dict: dict[str, str]) -> None:
    """

    Prompts the user for the value of all fields contained in
    the database_field collection.
    Adds a new entry to the data file based on the received values.
    For a new entry, the id is obtained by finding the number
    of entries in the file.

    """
    print(lang_dict.get('chosen_add_note', '__ERROR__'))
    person = {}

    for field, field_name in database_fields.items():
        message = lang_dict.get('input_note_data', '__ERROR__').format(field_name=field_name)
        field_value = validate_data_input(message, field, lang_dict)
        person[field] = field_value

    df = pd.read_csv('database.csv', index_col='pk')
    df.loc[len(df.index)] = person.values()

    print(lang_dict.get('note_add_success', '__ERROR__'))
    print(tabulate(df.tail(1), headers=['ID', *database_fields.values()]), end='\n\n')

    df.to_csv('database.csv')


def find_notes_handler(lang_dict: dict[str, str]) -> None:
    """

    Gets the query string by which the DataFrame filters.
    If nothing is found for the request, it notifies the user about this.

    """
    print(lang_dict.get('chosen_find_notes', '__ERROR__'))
    query = _get_query(lang_dict)

    df = pd.read_csv('database.csv')
    if len(df) == 0:
        print(lang_dict.get('bad_query', '__ERROR__'))
    else:
        print(tabulate(df.loc[df.query(query).index], headers=['ID', *database_fields.values()]))


def edit_notes_handler(lang_dict: dict[str, str]) -> None:
    """
    Gets the query string by which the DataFrame filters.
    If nothing is found for the request, it notifies the user about this.

    After receiving the filtered DataFrame, changes the required
    values of the records and saves the new value

    """
    print(lang_dict.get('chosen_find_notes', '__ERROR__'))
    query = _get_query(lang_dict)

    df = pd.read_csv('database.csv', index_col='pk')

    temp_df = df.loc[df.query(query).index]
    if len(temp_df) == 0:
        print(lang_dict.get('bad_query', '__ERROR__'))
    else:
        print()
        print(tabulate(temp_df.tail(5), headers=['ID', *database_fields.values()]), end='\n\n')

        new_fields = validate_change_input(database_fields, lang_dict)

        df.loc[df.query(query).index, new_fields.keys()] = tuple(new_fields.values())

        df.to_csv('database.csv')


def _get_query(lang_dict: dict[str, str]) -> tuple[str]:
    """

    Until the user decides to finish, new queries are requested.
    Then the function combines all received requests into one and returns it.

    """
    queries = []
    further = 'y'

    while further == 'y':
        query = validate_query_input(allowed_query_operations, lang_dict)
        queries.append(query)

        message = lang_dict.get('add_query', '__ERROR__')
        further = validate_command_input(message, options=['y', 'n'], lang_dict=lang_dict)

    union_query = f'({") & (".join(queries)})'
    return union_query


def exit_handler(lang_dict: dict[str, str]) -> None:
    print(lang_dict.get('exit_message', '__ERROR__'))
    exit()


database_fields = {
    'last_name': 'Last Name',
    'first_name': 'First Name',
    'middle_name': 'Middle Name',
    'organisation': 'Organisation',
    'official_number': 'Official Number',
    'personal_number': 'Personal Number',
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

# All commands specified in this collection become available to the user in the main menu
commands = {
    'help': show_tutorial_handler,
    'add_note': add_note_handler,
    'show_page': show_page_handler,
    'find_notes': find_notes_handler,
    'edit_notes': edit_notes_handler,
    'exit': exit_handler,
}
