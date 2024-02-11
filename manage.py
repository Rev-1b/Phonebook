from handlers import set_lang_handler, start_handler, choose_command_handler


def run():
    lang_dict = set_lang_handler()
    start_handler(lang_dict=lang_dict)

    while True:
        choose_command_handler(lang_dict=lang_dict)


if __name__ == '__main__':
    run()