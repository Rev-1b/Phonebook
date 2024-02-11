from languages import eng_lang, get_lang_codes, registered_languages
from utils.utils import get_lang_val
from validators import validate_command_input, validate_data_input
import pandas as pd

pd.set_option('display.max_columns', None)


def set_lang_handler() -> dict[str, str]:
    message = f'Good afternoon!\nBefore you start, select your interface language: {", ".join(get_lang_codes())} ... '
    lang_code = validate_command_input(message=message, options=get_lang_codes(), lang_dict=eng_lang)

    return registered_languages.get(lang_code.upper())


def start_handler(lang_dict: dict[str, str]) -> None:
    message = get_lang_val(key='start', lang_dict=lang_dict)
    show_tutorial = validate_command_input(message=message, options=['y', 'n'], lang_dict=lang_dict)
    if show_tutorial == 'y':
        show_tutorial_handler(lang_dict=lang_dict)


def show_tutorial_handler(lang_dict: dict[str, str]) -> None:
    tutorial_steps = ('short_description', 'show_list', 'add_note', 'find_notes', 'change_notes',)

    for step in tutorial_steps:
        message = get_lang_val(key=step, lang_dict=lang_dict)
        further = validate_command_input(message=message, options=['y', 'n'], lang_dict=lang_dict)

        if not further:
            break


def choose_command_handler(lang_dict: dict[str, str]) -> None:
    message = get_lang_val(key='require_input', lang_dict=lang_dict).format(commands=', '.join(commands.keys()))
    command = validate_command_input(message=message, options=commands.keys(), lang_dict=lang_dict)
    commands[command](lang_dict=lang_dict)


def show_list_handler(lang_dict: dict[str, str]) -> None:
    print(get_lang_val(key='chosen_show_list', lang_dict=lang_dict))
    db = pd.read_csv('database.csv', sep=',')
    print(db)


def add_note_handler(lang_dict: dict[str, str]) -> None:
    print(get_lang_val(key='chosen_add_note', lang_dict=lang_dict))
    person = {}

    for field, field_name in database_fields.items():
        message = get_lang_val(key='input_note_data', lang_dict=lang_dict).format(field_name=field_name)
        field_value = validate_data_input(message=message, field=field, lang_dict=lang_dict)
        person[field] = field_value

    db = pd.read_csv('database.csv', sep=',')
    db.loc[len(db.index)] = person.values()
    print()
    db.to_csv('database.csv', sep=',')



database_fields = {
    'last_name': 'Фамилия',
    'first_name': 'Имя',
    'middle_name': 'Отчество',
    'organisation': 'Имя Организации',
    'official_number': 'Рабочий номер',
    'personal_number': 'Личный номер',
}

commands = {
    'help': show_tutorial_handler,
    'add_note': add_note_handler,
    'show_list': show_list_handler,
}
