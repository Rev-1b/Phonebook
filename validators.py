from utils.utils import get_lang_val
import re


def _input_verified(command: str,
                    options: tuple[str],
                    lang_dict: dict[str, str]
                    ) -> bool:
    """

    """
    if command not in options:
        print(get_lang_val(key='notfound_command',
                           lang_dict=lang_dict
                           ).format(command=command,
                                    options=', '.join(options)))
        return False
    return True


def validate_show_input(pages: int, lang_dict: dict[str, str]) -> str:
    message = get_lang_val('chose_page', lang_dict).format(pages=pages)
    page = input(message)

    while page != 'exit' and (page not in map(str, range(pages))):
        pass




def validate_command_input(message: str,
                           options: list[str],
                           lang_dict: dict[str, str]
                           ) -> str:
    """


    """
    input_command = input(message).strip()

    while not _input_verified(command=input_command, options=options, lang_dict=lang_dict):
        input_command = input(get_lang_val(key='try_again', lang_dict=lang_dict)).strip()

    return input_command


def validate_data_input(message: str,
                        field: str,
                        lang_dict: dict[str, str]
                        ) -> str:
    """

    """
    field_value = input(message).strip()
    if field in ('personal_number', 'official_number'):
        pattern = re.compile(r"(0|91|\+7|8)?[6-9][0-9]{9}")

        while not pattern.match(field_value):
            field_value = input(get_lang_val(key='bad_phone_number', lang_dict=lang_dict)).strip()
    else:
        field_value = field_value.capitalize()

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

    message = (get_lang_val(message_key, lang_dict))

    if options is not None:
        message = message.format(options=', '.join(options))

    arg = input(message).strip()

    while options is not None and arg not in options:
        arg = input(get_lang_val(err_message_key, lang_dict)).strip()

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



    """
    raw_input = input(get_lang_val('change_fields', lang_dict).format(fields=fields.keys()))
    managed_data = raw_input.split()

    while any(field not in fields for field in managed_data):
        managed_data = input(get_lang_val('unexpected_field', lang_dict)).split()

    result = {}
    for field in managed_data:
        field_value = input(get_lang_val('change_field', lang_dict).format(field_name=fields[field]))
        result[field] = field_value

    return result


