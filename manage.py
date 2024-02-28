from handlers import SetLanguageHandler, StartHandler, ShowTutorialHandler, ChooseCommandHandler
from languages import eng_lang


def run(tutorial_steps):
    select_language_handler = SetLanguageHandler(eng_lang)
    language = select_language_handler.operation()

    start_handler = StartHandler(language)
    show_tutorial = start_handler.operation()
    if show_tutorial:
        show_tutorial_handler = ShowTutorialHandler(language, tutorial_steps)
        show_tutorial_handler.operation()

    while True:
        choose_command_handler = ChooseCommandHandler(language, tutorial_steps)
        command_class = choose_command_handler.operation()(language)
        command_class.operate(language)


if __name__ == '__main__':
    tutorial = ('short_description', 'show_page', 'add_note', 'find_notes', 'change_notes',)
    run(tutorial)
