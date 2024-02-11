from utils.utils import get_lang_val


def get_lang_codes() -> list[str]:
    return (get_lang_val(key='code', lang_dict=lang) for lang in _registered_languages)


ru_lang = {
    'code': 'RU',
    'choose_lang': f'Добрый день! Перед началом работы выберите язык интерфейса: {get_lang_codes()}',
    'start': 'Приветствие',
}

eng_lang = {
    'code': 'EN',
    'choose_lang': f'Good afternoon. Before you start, select your interface language: {get_lang_codes()}',
    'start': 'Приветствие',
}

_registered_languages = (
    ru_lang,
    eng_lang,
)


