from handlers import set_lang_handler


def run():
    lang_dict = set_lang_handler()


    with open('database.csv', newline='') as db:
        while True:
            pass


if __name__ == '__main__':
    run()