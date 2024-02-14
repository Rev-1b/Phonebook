from typing import Optional
import re


def _input_verified(command: str,
                    options: tuple[str],
                    lang_dict: dict[str, str]
                    ) -> bool:
    """

    Checks if what the user entered is an available command

    """
    if command not in options:
        print(lang_dict.get('notfound_command', '__ERROR__').format(command=command, options=', '.join(options)))
        return False
    return True


def validate_show_input(pages: int, lang_dict: dict[str, str]) -> Optional[str]:
    """

    Checks whether the user entered an existing page number or exit command.
    If a valid number is entered, returns it.

    When receiving the exit command, returns None

    """
    message = lang_dict.get('chose_page', '__ERROR__').format(pages=pages)
    page = input(message)

    while page not in ['exit', *map(str, range(1, pages + 1))]:
        if page.isdigit():
            page = input(lang_dict.get('bad_page', '__ERROR__'))
        else:
            page = input(lang_dict.get('bad_command', '__ERROR__'))

    return int(page) if page.isdigit() else None


def validate_command_input(message: str,
                           options: list[str],
                           lang_dict: dict[str, str]
                           ) -> str:
    """

    Requires you to enter the correct command until it gets it.

    """
    input_command = input(message).strip()

    while not _input_verified(input_command, options, lang_dict):
        input_command = input(lang_dict.get('try_again', '__ERROR__')).strip()

    return input_command


def validate_data_input(message: str,
                        field: str,
                        lang_dict: dict[str, str]
                        ) -> str:
    """

    The entered password must be verified using a regular expression.
    If a non-password field is entered, it is capitalized

    """
    field_value = input(message).strip()
    if field in ('personal_number', 'official_number'):
        regex = (r'^\+((?:9[679]|8[035789]|6[789]|5[90]|42|3[578]|2[1-689])|9[0-58]'
                 '|8[1246]|6[0-6]|5[1-8]|4[013-9]|3[0-469]|2[70]|7|1)(?:\W*\d){0,13}\d$')

        pattern = re.compile(regex)

        while not pattern.match(field_value):
            field_value = input(lang_dict.get('bad_phone_number', '__ERROR__')).strip()

    return field_value


def _get_query_obj(options: tuple[str],
                   message_key: str,
                   err_message_key: str,
                   lang_dict: dict[str, str]
                   ) -> str:
    """
    The function compares what the user enters with a list of valid values.

    If there is a discrepancy, it will require you to recheck the entered value.
    If the "options" parameter is None, no check occurs
    """

    message = (lang_dict.get(message_key, '__ERROR__'))

    if options is not None:
        message = message.format(options=', '.join(options))

    arg = input(message).strip()

    while options is not None and arg not in options:
        arg = input(lang_dict.get(err_message_key, '__ERROR__')).strip()

    return arg


def validate_query_input(allowed_operations: dict[str: tuple[str]],
                         lang_dict: dict[str, str]
                         ) -> tuple[str, list[str]]:
    """

    Calls '_get_query_obj' for 3 objects: filtered field, filter operation and filter operation argument
    Returns query string

    """
    main_arg = _get_query_obj(options=list(allowed_operations.keys()),
                              message_key='chose_first_arg',
                              err_message_key='first_arg_err',
                              lang_dict=lang_dict)

    operators = [i for tup in allowed_operations.values() for i in tup]
    operators = set(operators)

    operation = _get_query_obj(options=list(operators),
                               message_key='chose_operator',
                               err_message_key='operator_err',
                               lang_dict=lang_dict)

    sub_arg = _get_query_obj(options=None,
                             message_key='chose_sub_arg',
                             err_message_key='sub_arg_err',
                             lang_dict=lang_dict)

    return f'{main_arg}{operation}"{sub_arg}"'


def validate_change_input(fields: dict[str, str],
                          lang_dict: dict[str, str]
                          ) -> dict[str, str]:
    """

    Receives a raw string from the user, which should list all
    the fields to be changed separated by spaces.
    If at least one field is specified incorrectly, it requires
    you to enter a new value. Next, for each selected field, it
    prompts you to specify a new value.

    """
    raw_input = input(lang_dict.get('change_fields', '__ERROR__').format(fields=', '.join(fields.keys())))
    managed_data = raw_input.split()

    while any(field not in fields for field in managed_data):
        managed_data = input(lang_dict.get('unexpected_field', '__ERROR__')).split()

    result = {}
    for field in managed_data:
        field_value = input(lang_dict.get('change_field', '__ERROR__').format(field_name=fields[field]))
        result[field] = field_value

    return result
