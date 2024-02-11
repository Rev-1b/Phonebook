def get_lang_val(key: str, lang_dict: dict[str, str]) -> str:
    value = lang_dict.get(key, None)
    if value is None:
        raise ValueError(
            f'The language dictionary is incorrectly configured. Key "{key}" is missing.'
        )
    return value
