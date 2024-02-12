ru_lang = {
    'notfound_command': 'Проверьте введенное значение! Введенное "{command}" не соответствует списку допустимых '
                        'значений "{options}".\n',
    'try_again': 'Попробуйте еще раз: ',
    'start': 'Добро пожаловать в приложение "Интерактивная телефонная книга"!\n\n'
             'Перед тем, как начать, предлагаем пройти короткое обучение, в котором будет показано, как пользоваться '
             'программой.\n\nХотите пройти обучение? y/n ... ',

    'short_description': 'Краткое описание ... \n\nХотите продолжить? y/n ... ',
    'show_list': 'Показать страницу... \n\nХотите продолжить? y/n ... ',
    'add_note': 'Добавить запись ... \n\nХотите продолжить? y/n ... ',
    'find_notes': 'Найти записи ... \n\nХотите продолжить? y/n ... ',
    'change_notes': 'Изменить записи ... \n\nХотите продолжить? y/n ... ',

    'require_input': 'Выберите действие: "{commands}" ...',

    'chosen_show_list': 'Отображение страницы: \n\n',

    'chosen_add_note': 'Добавление новой записи:\n\n',
    'input_note_data': 'Пожалуйста, введите {field_name}: ... ',
    'bad_phone_number': 'Введенный номер "{}" некорректен. Попробуйте снова: ... ',
    'note_add_success': 'Вы успешно добавили новую запись в книгу: \n',

    'chosen_find_notes': 'Нахождение записей:\n\n',
    'add_query': 'Хотите добавить еще одно условие фильтрации? y/n ... ',
}

eng_lang = {
    'notfound_command': 'Проверьте введенное значение! Введенное {command} не соответствует списку допустимых '
                        'значений {options}.\n',
    'try_again': 'Попробуйте еще раз: ',
    'start': 'Добро пожаловать в приложение "Интерактивная телефонная книга"!\n\n'
             'Перед тем, как начать, предлагаем пройти короткое обучение, в котором будет показано, как пользоваться'
             'программой.\n\nХотите пройти обучение? y/n ... ',
    'short_description': 'Краткое описание',
    'show_list': 'Показать страницу... \n\nХотите продолжить? y/n ... ',
    'add_note': 'Добавить запись ... \n\nХотите продолжить? y/n ... ',
    'find_notes': 'Найти записи ... \n\nХотите продолжить? y/n ... ',
    'change_notes': 'Изменить записи ... \n\nХотите продолжить? y/n ... ',
    'require_input': 'Введите команду: ...'
}

registered_languages = {
    'RU': ru_lang,
    'ENG': eng_lang,
}


def get_lang_codes() -> list[str]:
    return [code for code in registered_languages]
