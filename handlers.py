from languages import eng_lang, get_lang_codes, registered_languages
from utils.utils import get_lang_val
from validators import validate_input


def set_lang_handler() -> dict[str, str]:
    message = f'Good afternoon!\nBefore you start, select your interface language: {", ".join(get_lang_codes())} ... '
    lang_code = validate_input(message=message, options=get_lang_codes(), lang_dict=eng_lang)

    return registered_languages.get(lang_code.upper())


def start_handler(lang_dict: dict[str, str]) -> None:
    message = get_lang_val(key='start', lang_dict=lang_dict)
    show_tutorial = validate_input(message=message, options=['y', 'n'], lang_dict=lang_dict)
    if show_tutorial == 'y':
        pass
    else:
        pass


def show_tutorial_handler(lang_dict: dict[str, str]) -> None:








commands = {
    'help': ''
}
