from utils.utils import get_lang_val
import re


def _input_verified(command: str, options: tuple[str], lang_dict: dict[str, str]) -> bool:
    if command not in options:
        print(get_lang_val(key='notfound_command', lang_dict=lang_dict).format(command=command,
                                                                               options=', '.join(options)))
        return False
    return True


def validate_command_input(message: str, options: list[str], lang_dict: dict[str, str]) -> str:
    input_command = input(message)

    while not _input_verified(command=input_command, options=options, lang_dict=lang_dict):
        input_command = input(get_lang_val(key='try_again', lang_dict=lang_dict))

    return input_command


def validate_data_input(message: str, field: str, lang_dict: dict[str, str]) -> str:
    field_value = input(message)
    if field in ('personal_number', 'official_number'):
        pattern = re.compile(r"(0|91|\+7|8)?[6-9][0-9]{9}")

        while not pattern.match(field_value):
            field_value = input(get_lang_val(key='bad_phone_number', lang_dict=lang_dict))

    else:
        field_value = field_value.capitalize()

    return field_value


def validate_query_input(lang_dict: dict[str, str]) -> list[str]:
    pass
